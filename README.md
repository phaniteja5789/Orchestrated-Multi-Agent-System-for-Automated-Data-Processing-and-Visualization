# MultiAgentSystem_LangGraph

This Repository contains the code for the functionality of Multi Agent System using LangGraph as a framework.

I have created 3 Agents and a SuperVisor Agent

  1.) Extractor
  2.) Analyzer
  3.) Visualizer

Supervisor Agent connects to Extractor,Analyzer and Visualizer Agents, This Supervisor Agents is responsible which Agents to act next based on the State of the Workflow

Extractor Agent ==> This Agent is responsible for extracting the details from the URL.
                    The details are extracted from this URL (https://randomuser.me/api)
                    The extracted details will be present in JSON format. From the details, I am extracting necessary information like Name,Country,Gender etc.
                    Once the necessary details has been extracted, I have created a Tool(RequestAndInsertionTool.py) which inserts the details into the Postgres Database "Person" Table.
                    Once the details has been inserted into the Postgres Table using Psycopg2 module, the result code information will be sent to the Supervisor

Analyzer Agent ==> This Agent is responsible for generating a SQL Query and Analyzing the query and execute the SQL Query
                   It uses the existing SQLDatabase Toolkit from the Langchain in order to execute the Query
                   I have created a workflow in QueryGenerator.py which has 2 Nodes (Query_Gen_Node, invoke_tool) and added the edges.
                   The Query_Gen_Node ==> This Node is used to generate the SQL Query
                   Invoke_tool ==> This tool will use tool_calls and execute the SQL Query generated and return the result.
                   I have used a state called SQLState which tracks the messages between the nodes of the workflow of SQLAgent Workflow which is called as Analyzer Agent

Visualizer Agent ==> This Agent is resposible for generating a Matplotlib Graph based on the result
                     It uses PythonREPL Tool, which is used to generate the code and generate the MatplotLib Chart


Supervisor Agent ==> A static System Prompt is used which has members (Extractor, Analyzer,Visualizer) and it also uses the NEXT in order to choose which Agent needs to be invoked based on the Input Text
                     It uses the tool calling which has function "Route" which determines which Agent to invoke.
                     Creation_Of_Supervisor_Chain ==> which is used to create a chain which has System Prompt and a LLM which bind the tools and return the Chain.                     
                     


SourceCode.py ==> This is the entry point for the execution of the multi agent
In SourceCode.py, I have created a workflow where it is responsible for creation of nodes and creation of agents

In Agent_Creation.py ==> This class is responsible for creating the Agent, which takes the arguments as LLM,tools,system_prompt
                        LLM ==> It is responsible for using any LLM Model
                        tools ==> LLM will use the list of tools that Agent needs to use 
                        System_Prompt ==> Each Agent is responsible for doing a Specific task with a set of tools and the LLM.

In Node_Creation.py ==> This class is responsible for creating the Node which takes the arguments AgentState,Agent and the Name of the Agent
                        AgentState ==> This is used to keep track of the messages that the agents keep tracks
                        Agent ==> Agents that we created earlier, the Node_Creation.py is mainly used to invoke the Agent which implements the Runnable Interface
                        Name ==> Name of the Agent(Eg: Extractor,Analyzer and Visualizer etc)

The Entire workflow will be created in the SourceCode.py, with the Extractor,Analyzer and Visualizer Nodes which invokes based on the Supervisor Request

Supervisor will use Tool Calling, in order to decide which Agent to execute next.

Based on the Next, the request will be sent to the Node and the Node will invoke the Agent based on the Agent State Messages which is used to track the messages in between the Nodes present in the Workflow.

The Workflow is as below graph,


![output](https://github.com/user-attachments/assets/d0d544c6-6d15-49b4-ae5f-7f2ffde2c66e)

Once the entire request has been processed, the Supervisor will send the messages as "FINISH" which stops the execution.


Frameworks used ==> LangChain, LangGraph
LLMs used ==> OpenAI



