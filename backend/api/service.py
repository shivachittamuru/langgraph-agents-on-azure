import os
import json
from uuid import uuid4
from typing import AsyncGenerator, Dict, Any, List, Tuple

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import logging

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.graph import CompiledGraph

from api.settings import app_settings as settings
from api.schema import UserInput, AgentResponse, ChatMessage, StreamInput

import asyncio
import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection

from agents.checkpointer import get_sqlite_checkpointer, get_async_sqlite_checkpointer
from agents.tracing import tracer, root_span
from agents.sql_agent.sql_agent import AzureSqlAgent
from agents.sql_agent.tools import db_query_tool, list_tables_tool, get_schema_tool




@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the lifespan of the FastAPI application to define application startup and shutdown logic.
    
    Parameters:
    app (FastAPI): The FastAPI application instance.
    """
    try:
        llm = AzureChatOpenAI(  
                api_key=settings.azure_openai_key,  
                azure_endpoint=settings.azure_openai_endpoint,  
                api_version=settings.azure_openai_api_version,  
                azure_deployment=settings.azure_openai_deployment_name,
                streaming=True,  
                temperature=0,
            )  

        ###########
        # SQLite Checkpointer
        ############
        # # checkpointer = get_sqlite_checkpointer()  # sync version
        
        # async version
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
        db_path = os.path.join(base_dir, "checkpointer_db", "state.db")
        
        
        async with aiosqlite.connect(db_path) as conn:
            checkpointer = AsyncSqliteSaver(conn=conn)     
        
        #############
        # Postgres Checkpointer
        #############
        
        # host = settings.host
        # user = settings.user
        # password = settings.password
        # database = settings.database

        # DB_URI = (
        #     f"dbname={database} user={user} password={password} host={host} port=5432"
        # )

        # connection_kwargs = {
        #     "autocommit": True,
        #     "prepare_threshold": 0,
        # } 
        
        # async with await AsyncConnection.connect(DB_URI, **connection_kwargs) as conn:
        #     checkpointer = AsyncPostgresSaver(conn=conn)
                        
            # SQL Agent setup
            tools = [db_query_tool]
            sql_agent = AzureSqlAgent(llm=llm, tools=tools, checkpointer=checkpointer)        
            app.state.sql_agent = sql_agent 
            
            yield        
        
    except Exception as e:
        print(f"Exception in lifespan context manager: {e}")
        raise HTTPException(status_code=500, detail=str(e))       

        
        
app = FastAPI(lifespan=lifespan)


# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_sql_agent():
    sql_agent = app.state.sql_agent
    if sql_agent is None:
        raise HTTPException(status_code=500, detail="Sql Agent is not available.")
    return sql_agent


@app.get("/health")
async def health():
    """Check the api is running"""
    return {"status": "🤙"}



def _parse_input(user_input: UserInput) -> Tuple[Dict[str, Any], str]:
    run_id = str(uuid4())
    thread_id = user_input.thread_id or str(uuid4())
    print(f"run ID: {run_id} in _parse_input fn.")
    print(f"thread ID: {thread_id} in _parse_input fn.")
    input_message = ChatMessage(type="human", content=user_input.message)
    print(f"Input Message: {input_message}")
    kwargs = dict(
        input = {"messages": [input_message.to_langchain()]}, # For response_model=ChatMessage
        # input = {"messages": [HumanMessage(content=user_input.message)]},   # For response_model=AgentResponse  
        config = RunnableConfig(
            configurable={"thread_id": thread_id},
            run_id=run_id,
        ),
    )
    print(f"Kwargs: {kwargs}")
    return kwargs, run_id


@app.post("/sql-invoke", response_model=ChatMessage)
async def invoke_sql_agent(input: UserInput, sql_agent: AzureSqlAgent = Depends(get_sql_agent)): 
    """
    Invoke the sql agent with user input to generate a query response.
    Use thread_id to persist and continue a multi-turn conversation. 
    """
    kwargs, run_id = _parse_input(input)
    try:
        with root_span(tracer=tracer, name = "API-Invoke-SqlAgent" + " - " + input.message, agent="AzureSqlAgent") as root:
            thread_id = kwargs["config"]["configurable"]["thread_id"]
            root.set_attribute("thread_id", str(thread_id))
            # result = sql_agent.graph.invoke(**kwargs) # sync version
            result = await sql_agent.graph.ainvoke(**kwargs)    # async version
        response = result["messages"][-1]  
        output = ChatMessage.from_langchain(response)
        output.run_id = str(run_id)
        return output   # converts langchain response AIMessage to ChatMessage
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


