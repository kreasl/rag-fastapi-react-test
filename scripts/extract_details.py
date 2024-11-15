import pprint

from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, HumanMessage

from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from ai.agent import agent
from ai.generator import generate
from ai.retriever import get_retriever_tool

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

retrieve = ToolNode([get_retriever_tool()])

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.add_edge(START, "agent")
workflow.add_edge("agent", "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

graph = workflow.compile()

inputs = {
    "messages": [
        HumanMessage("Give me a link to Applicant's LinkedIn profile")
    ]
}

for output in graph.stream(inputs):
    for key, value in output.items():
        pprint.pprint(f"Output from node '{key}':")
        pprint.pprint("---")
        pprint.pprint(value, indent=2, width=80, depth=None)
    pprint.pprint("\n--\n")

