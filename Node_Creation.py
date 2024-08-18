from langchain_core.messages import BaseMessage, HumanMessage


## Creation of each node for the langgraph, where the agent will invoke based on the input recieved
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}