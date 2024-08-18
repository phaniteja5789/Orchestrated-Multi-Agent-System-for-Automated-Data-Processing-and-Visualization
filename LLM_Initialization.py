from langchain_openai import ChatOpenAI


def llm_initialization():

    ## Model Initialization
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", streaming=True,api_key="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")
    return llm