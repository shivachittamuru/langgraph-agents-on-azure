from pydantic import BaseModel, Field
from langchain_core.tools import tool

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import AzureChatOpenAI

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

llm = AzureChatOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],   # tool_choice="required" is only supported in 2024-06-01 and later
    azure_deployment="gpt-4o",
    streaming=True,
    temperature=0
)



db = SQLDatabase.from_uri("sqlite:///chinook.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

class GenerateQuery(BaseModel):
    """Generate a query based on the question and schema."""
    query: str = Field(..., description="The generated query to run on the sqlite3 database.")


@tool(args_schema=GenerateQuery)
def db_query_tool(query: str) -> str:
    """
    Execute a SQL query against the database and get back the result.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    
    # db = SQLDatabase.from_uri("sqlite:///sample.db")
    
    result = db.run_no_throw(query)
    
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    if result.startswith("Error:"):
        return result + "\nPlease rewrite your query and try again."
    return result   # above if condition is not required as "run_no_throw returns error too"



list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")


# sql_query = db_query_tool.invoke('SELECT * FROM Artist LIMIT 10;')
# print(sql_query)

# Run from /backend folder
# python -m agents.sql_agent.tools