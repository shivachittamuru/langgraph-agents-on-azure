from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END

from agents.visualization_agent.prompts import VISUAL_HUMAN_PROMPT, VISUAL_SYSTEM_PROMPT
from agents.visualization_agent.chart_schema import PlotlyChart
from agents.checkpointer import get_sqlite_checkpointer, get_async_sqlite_checkpointer
from agents.tracing import tracer, root_span

import asyncio
import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import os
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)


class VisualizationAgent:
    def __init__(self, llm, checkpointer=None):
        self.llm = llm
        self.checkpointer = checkpointer
    
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("visualization_extraction", self.visualization_node)
        graph_builder.add_edge(START, "visualization_extraction")
        graph_builder.add_edge("visualization_extraction", END)
        
        if checkpointer:
            self.graph = graph_builder.compile(checkpointer=checkpointer)
        else:
            self.graph = graph_builder.compile()

    async def visualization_node(self, state: MessagesState):
        with tracer.start_as_current_span("visualization_agent_node") as span:
            messages = state["messages"]

            questions = [msg for msg in messages if msg.type == 'human' and msg.name is None]
            latest_question = questions[-1].content
            query_response = messages[-1].content
            # print(f"\nLatest Question: {latest_question}")
            # print(f"\nQuery Response: {query_response}")
            
            span.set_attribute("input.question", latest_question)
            span.set_attribute("input.sql_response", query_response)

            visual_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", VISUAL_SYSTEM_PROMPT),
                    ("human", VISUAL_HUMAN_PROMPT)
                ]
            )
            structured_llm = self.llm.with_structured_output(PlotlyChart)
            visual_llm = visual_prompt | structured_llm

            visual_response_object = await visual_llm.ainvoke({'user_input': latest_question, 'query_output': query_response})
            visual_response_json = visual_response_object.model_dump(exclude_none=True)
            visual_response_str = json.dumps(visual_response_json)
            
            span.set_attribute("output.plotly_json", visual_response_str)
            
            visual_ai_msg = AIMessage(content=visual_response_str)
            return {"messages": [visual_ai_msg]}
    

async def main():
    import uuid

    llm = AzureChatOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],   # tool_choice="required" is only supported in 2024-06-01 and later
        azure_deployment="gpt-4o",
        streaming=True,
        temperature=0
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
    db_path = os.path.join(base_dir, "..", "checkpointer_db", "state.db")

    async with aiosqlite.connect(db_path) as conn:
        checkpointer = AsyncSqliteSaver(conn=conn)
        agent = VisualizationAgent(llm,checkpointer)

        session_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": session_id}}
        print(f"Session ID: {session_id}\n")
        
        query_output = "Value Sales of Bitesize in YTD: 62508617.07 \
                    Volume Sales of Bitesize in YTD: 5906528.78 \
                    Value Sales of SweetPeak Confections Bitesize in YTD: 41310609.21 \
                    Volume Sales of SweetPeak Confections Bitesize in YTD: 3277883.07"
        user_input = "what is my YTD sales performance wrt bitesize?"
        messages = [HumanMessage(content=user_input)] + [HumanMessage(content=query_output)]
        result = await agent.graph.ainvoke(
            {"messages": messages},
            config=config
        )
        print(result['messages'][-1].content)



if __name__ == '__main__':
    asyncio.run(main())

# RUN from /backend directory
# python -m agents.visualization_agent.visualization_agent