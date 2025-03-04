import os  
import asyncio  
from typing import Annotated, Literal, Any
from typing_extensions import TypedDict  
from pydantic import BaseModel, Field  
 
from langchain_core.prompts import ChatPromptTemplate  
from langchain_openai import AzureChatOpenAI  
from langgraph.graph import END, StateGraph, START  
from langgraph.graph.message import MessagesState, AnyMessage, add_messages, RemoveMessage
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage 
from langchain_core.runnables import RunnableLambda, RunnableWithFallbacks
from langgraph.prebuilt import ToolNode

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection

from agents.sql_agent.tools import db_query_tool, list_tables_tool, get_schema_tool
from agents.sql_agent.prompts import QUERY_AGENT_SYSTEM_MSG  
from agents.checkpointer import get_sqlite_checkpointer, get_async_sqlite_checkpointer   
from agents.tracing import tracer, root_span

from dotenv import load_dotenv, find_dotenv  
load_dotenv(find_dotenv(), override=True)  

# import logging
# logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
  
# The following is handled by MessagesState 
# class MessagesState(TypedDict):  
#     messages: Annotated[list[AnyMessage], add_messages]  
  

class AzureSqlAgent:
    def __init__(self, llm, tools, checkpointer=None):   
        """
        Initialize the Azure SQL Agent.

        Args:
            llm: The language model instance.
            tools: A list of tools the agent can use.
            checkpointer: Optional checkpointer for state persistence.
        """     
        try:
            graph_builder = StateGraph(MessagesState)
            
            graph_builder.add_node("list_tables_ai_call", self.list_tables_ai_call)
            graph_builder.add_node(
                "list_tables_tool", self.create_tool_node_with_fallback([list_tables_tool])
            )

            graph_builder.add_node("get_relevant_schema", self.get_db_schema)
            graph_builder.add_node("get_schema_tool", self.create_tool_node_with_fallback([get_schema_tool]))
            
            graph_builder.add_node("query_agent", self.query_agent_node)
            graph_builder.add_node("execute_query", self.db_tool_node)
            graph_builder.add_node("delete_intermediate_messages", self.delete_intermediate_messages)
            graph_builder.add_node("rolling_window", self.rolling_window)
            
            graph_builder.add_edge(START, "list_tables_ai_call")
            graph_builder.add_edge("list_tables_ai_call", "list_tables_tool") 
            graph_builder.add_edge("list_tables_tool", "get_relevant_schema")
            graph_builder.add_edge("get_relevant_schema", "get_schema_tool")
            graph_builder.add_edge("get_schema_tool", "query_agent")
            graph_builder.add_conditional_edges(
                "query_agent",
                self.tool_check,
                # {"query_db": "execute_query", "__end__": END}
                {"query_db": "execute_query", "generate_answer": "delete_intermediate_messages"}
            )
            graph_builder.add_edge("execute_query", "query_agent")   
            graph_builder.add_edge("delete_intermediate_messages", "rolling_window")
            graph_builder.add_edge("rolling_window", END)
            
            if checkpointer:
                self.graph = graph_builder.compile(checkpointer=checkpointer) 
            else:
                self.graph = graph_builder.compile()  
                
            self.tools = tools
            self.tools_mapping = {t.name: t for t in tools}
            self.llm = llm
            self.llm_with_tools = llm.bind_tools(tools)
            
        except Exception as e:
            # logging.error(f"Error initializing AzureSqlAgent: {e}")
            print(f"Error initializing AzureSqlAgent: {e}")
            raise
        
    def create_tool_node_with_fallback(self, tools: list) -> RunnableWithFallbacks[Any, dict]:
        """
        Create a ToolNode with a fallback to handle errors and surface them to the agent.
        """
        return ToolNode(tools).with_fallbacks(
            [RunnableLambda(self.handle_tool_error)], exception_key="error"
        )


    def handle_tool_error(self, state: MessagesState) -> dict:
        error = state.get("error")
        tool_calls = state["messages"][-1].tool_calls
        return {
            "messages": [
                ToolMessage(
                    content=f"Error: {repr(error)}\n please fix your mistakes.",
                    tool_call_id=tc["id"],
                )
                for tc in tool_calls
            ]
        }
        
    def delete_intermediate_messages(self, state: MessagesState):
        return {"messages": [RemoveMessage(id=msg.id) for msg in state['messages']  if (msg.type == "tool" or msg.content=="")]}   
        # return {"messages": [RemoveMessage(id=msg.id) for msg in state['messages']  if (msg.type == "tool" or (msg.type =="ai" and msg.tool_calls))]}

    def rolling_window(self, state: MessagesState):
        n_msgs=6
        return {"messages": [RemoveMessage(id=msg.id) for msg in state['messages'][:-n_msgs]]}

    # Add a node for the first tool call
    def list_tables_ai_call(self, state: MessagesState) -> dict[str, list[AIMessage]]:
        return {
            "messages": [
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "sql_db_list_tables",
                            "args": {},
                            "id": "tool_abcd123",
                        }
                    ],
                )
            ]
        }
        
        
    async def get_db_schema(self, state: MessagesState):  
        model_get_schema  = self.llm.bind_tools([get_schema_tool])
        
        messages = state["messages"]
        db_schema = await model_get_schema.ainvoke(messages)
        return {"messages": [db_schema]}
    

    async def query_agent_node(self, state: MessagesState):
        """
        Handle the query_agent node in the state graph.

        Args:
            state: The current state of the graph.

        Returns:
            Updated state with the query response.
        """  
        try:
            with tracer.start_as_current_span("query_agent_node") as span:              
                query_agent_prompt = ChatPromptTemplate.from_messages(
                    [("system", QUERY_AGENT_SYSTEM_MSG), ("human", "{messages}")]
                )    
                query_agent = query_agent_prompt | self.llm_with_tools  # tools = [db_query_tool]
                
                messages = state["messages"]
                questions = [msg for msg in messages if msg.type == 'human' and msg.name is None]
                latest_question = questions[-1].content if questions else None
                span.set_attribute("input.question", str(latest_question)) 
                
                query_response = await query_agent.ainvoke({'messages': messages})
                
                if len(query_response.tool_calls) > 0:
                    for tc in query_response.tool_calls:
                        span.set_attribute("output.query", str(tc['args']['query']))
                else:
                    span.set_attribute("output.answer", str(query_response.content))
                
                # print(f"Query Response: {query_response}")
                return {"messages": [query_response]}
        except Exception as e:
            # logging.error(f"Error in query_agent_node: {e}")
            print(f"Error in query_agent_node: {e}")
            return {"messages": [AIMessage(content="An error occurred: {e}. Please retry.")]}

    async def db_tool_node(self, state: MessagesState):
        """
        Handle the query_agent node in the state graph.

        Args:
            state: The current state of the graph.

        Returns:
            Updated state with the query response.
        """
        try:
            with tracer.start_as_current_span("db_tool_node") as span:            
                tool_calls = state["messages"][-1].tool_calls                
                results = []   
                    
                for tool_call in tool_calls:
                    # print(f"Calling: {tool_call}")
                    if not tool_call['name'] in self.tools_mapping.keys():     # check for bad tool name from LLM
                        print("\n ....bad tool name....")
                        span.set_attribute("input.tool_name", str(tool_call["name"]))
                        output = "bad tool name, retry"  # instruct LLM to retry
                        span.set_attribute("output.error", str(output))
                    else:
                        tool = self.tools_mapping[tool_call["name"].lower()]
                        span.set_attribute("input.tool_name", str(tool_call["name"]))
                        span.set_attribute("input.query", str(tool_call["args"]["query"]))
                        output = await tool.ainvoke(tool_call["args"])   
                        span.set_attribute("output.db_result", str(output))   
                        
                    results.append(ToolMessage(
                        tool_call_id=tool_call['id'], 
                        name=tool_call['name'], 
                        content=str(output)
                    ))
                # print(f"Tool Results: {results}")
                
                state['messages'] = results
                return state
        except Exception as e:
            # logging.error(f"Error in db_tool_node: {e}")
            print(f"Error in db_tool_node: {e}")
            return state  # Graceful fallback without changing state


    def tool_check(self, state: MessagesState) -> Literal["query_db", "generate_answer"]:
        last_message = state["messages"][-1]        
        return "query_db" if last_message.tool_calls else "generate_answer" 
    
    
def get_postgres_db_uri() -> str:
    host = os.getenv("PG_VECTOR_HOST")
    user = os.getenv("PG_VECTOR_USER")
    password = os.getenv("PG_VECTOR_PASSWORD")
    database = os.getenv("PGDATABASE")

    DB_URI = (
        f"dbname={database} user={user} password={password} host={host} port=5432"
    )
    return DB_URI
    
    

async def main():  
    llm = AzureChatOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],   # tool_choice="required" is only supported in 2024-06-01 and later
        azure_deployment="gpt-4o",
        streaming=True,
        temperature=0
    )  
    tools = [db_query_tool, list_tables_tool, get_schema_tool]  

    ###########
    # SQLite Checkpointer
    ############
    
    import aiosqlite
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
    db_path = os.path.join(base_dir, "..", "checkpointer_db", "state.db")
    # print (f"DB Path: {db_path}")
    
    async with aiosqlite.connect(db_path) as conn:
        checkpointer = AsyncSqliteSaver(conn=conn)
    
        
        # Create an instance of AzureSqlAgent with the checkpointer  
        sql_agent = AzureSqlAgent(llm=llm, tools=tools, checkpointer=checkpointer)  
        
        import uuid  
        session_id = str(uuid.uuid4())  
        config = {"configurable": {"thread_id": session_id}}  
        print(f"Session ID: {session_id}\n")  
        
        # user_input = "Get the first 10 tracks with the genre 'Rock'"
        # user_input = " Finding the top 5 artists with the most albums:"
        user_input = "Find albums released by artists who have more than 5 albums"
    
        with root_span(tracer=tracer, name = "AzureSqlAgent-PythonClass" + " - " + user_input, agent="Azure SQL Agent"):
            result = await sql_agent.graph.ainvoke(  
                {"messages": [HumanMessage(content=user_input)]},  
                config=config  
                # {"recursion_limit": 10}  
            )  
        
        print("\nMessages:")  
        for m in result['messages']:  
            if m.content == '':  
                print(f"{m.type}: {m.tool_calls}")  
            else:  
                print(f"{m.type}: {m.content}")  
        print(f"\nTotal number of messages: {len(result['messages'])}\n")  

  
if __name__ == "__main__":  
    asyncio.run(main())  
    
# RUN
# python -m agents.sql_agent.sql_agent