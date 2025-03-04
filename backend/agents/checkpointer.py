import os

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

import asyncio
import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


def get_sqlite_checkpointer():    
    try:
        # Build absolute path to state.db
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
        db_path = os.path.join(base_dir, "checkpointer_db", "state.db")
        
        # Ensure the directory exists
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found at: {db_path}")

        # Connect to the database
        conn = sqlite3.connect(db_path, check_same_thread=False)
        checkpointer = SqliteSaver(conn=conn)
        return checkpointer
    except Exception as e:
        print(f"Error setting up Sqlite checkpointer: {e}")
        raise
    

    

async def get_async_sqlite_checkpointer():   
    
    try:
        # Build absolute path to state.db
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
        db_path = os.path.join(base_dir, "checkpointer_db", "state.db")
        print(f"DB Path: {db_path}")
        
        # Ensure the directory exists
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found at: {db_path}")

        # # Connect to the database
        # conn = await aiosqlite.connect(db_path)
        # print(f"Connection: {conn}")
        # checkpointer = AsyncSqliteSaver(conn=conn)
        # print(f"Checkpointer: {checkpointer}")
        # return checkpointer
        
        # Use 'async with' for resource management
        async with aiosqlite.connect(db_path) as conn:
            print(f"Connection: {conn}")
            # Create AsyncSqliteSaver within the context
            checkpointer = AsyncSqliteSaver(conn=conn)
            print(f"Checkpointer: {checkpointer}")
            print(f"Checkpointer connection: {checkpointer.conn}")
            if checkpointer.conn is None:
                print("Checkpointer connection is not initialized.")
            return checkpointer  # Only return AsyncSqliteSaver
        
    except Exception as e:
        print(f"Error setting up Async Sqlite checkpointer: {e}")

  
# async def get_async_sqlite_checkpointer():  
#     try:  
#         base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script  
#         db_path = os.path.join(base_dir, "checkpointer_db", "state.db")  
  
#         # Ensure the directory exists  
#         os.makedirs(os.path.dirname(db_path), exist_ok=True)  
  
#         # Use 'async with' for resource management  
#         async with aiosqlite.connect(db_path) as conn:  
#             checkpointer = AsyncSqliteSaver(conn=conn)  
#             await checkpointer.setup()  
#             return checkpointer  
#     except Exception as e:  
#         print(f"Error setting up Async Sqlite checkpointer: {e}")  
#         raise  
    
    
async def test_async_sqlite_checkpointer():
    # Test the checkpointer initialization
    try:
        print("Testing Async Sqlite Checkpointer...")
        checkpointer = await get_async_sqlite_checkpointer()

        # Optional: Perform a basic operation to test the checkpointer further
        print(f"Checkpointer available methods: {dir(checkpointer)}")

        # Placeholder for an actual operation
        if hasattr(checkpointer, 'get_next_version'):
            print("The checkpointer has 'get_next_version' method.")
        else:
            print("The 'get_next_version' method is not available on the checkpointer.")

    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        print("Test complete.")



if __name__ == "__main__":
    asyncio.run(test_async_sqlite_checkpointer())

    
    
## RUN
# python -m agents.checkpointer