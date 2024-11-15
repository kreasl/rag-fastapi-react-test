from langchain_openai import ChatOpenAI

from .retriever import get_retriever_tool

tools = [get_retriever_tool()]

def agent(state):
    print("---CALL AGENT---")
    messages = state["messages"]
    model = ChatOpenAI(temperature=0, streaming=True, model_name="gpt-3.5-turbo")
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": [response]}

