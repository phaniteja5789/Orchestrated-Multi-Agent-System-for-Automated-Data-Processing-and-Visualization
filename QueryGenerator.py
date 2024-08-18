from langchain.pydantic_v1 import BaseModel,Field
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
import json
from LLM_Initialization import llm_initialization
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from DBQueryTool import get_db_connection_string
import DBQueryTool
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import AnyMessage, add_messages
from typing import Annotated,Sequence, TypedDict


# Creating a subgraph for the SQL Agent to Analyze the Database and get the results from the database table

# Define the state for the agent
class SQLState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


llm = llm_initialization()
db = get_db_connection_string()
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()


# Describe a tool to represent the end state
class SubmitFinalAnswer(BaseModel):
    """Submit the final answer to the user based on the query results."""

    final_answer: str = Field(..., description="The final answer to the user")

query_gen_system = """You are a SQL expert with a strong attention to detail.

Given an input question, output a syntactically correct SQLite query to run, then look at the results of the query and return the answer from the Person table.

DO NOT call any tool besides SubmitFinalAnswer to submit the final answer.

When generating the query:

Output the SQL query that answers the input question without a tool call.

Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.

If you get an error while executing a query, rewrite the query and try again.

If you get an empty result set, you should try to rewrite the query to get a non-empty result set. 
NEVER make stuff up if you don't have enough information to answer the query... just say you don't have enough information.

If you have enough information to answer the input question, simply invoke the appropriate tool to submit the final answer to the user.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database."""

query_gen_prompt = ChatPromptTemplate.from_messages(
    [("system", query_gen_system), ("placeholder", "{messages}")]
)

query_gen = query_gen_prompt | llm.bind_tools(
    [SubmitFinalAnswer, DBQueryTool.db_query_tool]
)

def invoke_tool(state : SQLState):
    
    tool_calls = state['messages'][-1].additional_kwargs.get("tool_calls", [])

    # Convert tool_calls to a format compatible with the 'tools' structure
    tools = []
    for tool_call in tool_calls:
        tools.append({
            "name": tool_call["function"]['name'],
            "arguments": tool_call["function"]["arguments"]
        })
    
    for tool in tools:
        if tool["name"] == 'db_query_tool' :
            query_dict = json.loads(tool["arguments"])
            result = DBQueryTool.db_query_tool.invoke(query_dict["query"])
            print(result)
            state['messages'].append(AIMessage(result))

def query_gen_node(state: SQLState):
    message = query_gen.invoke(state)
    return {"messages": [message]}


# Define a new graph

sql_agent_workflow = StateGraph(SQLState)

sql_agent_workflow.add_node("query_gen", query_gen_node)
sql_agent_workflow.add_node("tool_node",invoke_tool)

sql_agent_workflow.add_edge(START,"query_gen")
sql_agent_workflow.add_edge("query_gen","tool_node")
sql_agent_workflow.add_edge("tool_node",END)

# Compile the workflow into a runnable
app = sql_agent_workflow.compile()


## Graph Stream
for s in app.stream(
    {
        "messages": [
            HumanMessage(content="""
                         Analyze the number of people based on their gender """)
        ]
    }
):
    if "__end__" not in s:
        print(s)
        print("----")



def get_sql_flow():
    return app