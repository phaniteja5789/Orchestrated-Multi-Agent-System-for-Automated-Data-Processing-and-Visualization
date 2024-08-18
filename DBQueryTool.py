from langchain_community.utilities import SQLDatabase
from langchain.tools import BaseTool,StructuredTool,tool


db = SQLDatabase.from_uri("postgresql://postgres:Phaniteja5789%40@localhost:5432/agent")

@tool
def db_query_tool(query: str):
    """
    Execute a SQL query against the database and get back the result.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    result = db.run_no_throw(query)
    print(result)
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    return result


def get_db_connection_string():
    return db