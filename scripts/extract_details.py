import os.path
import pprint

from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict
from pypdf import PdfReader

from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition, ToolNode

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def read_pdf(path: str):
    reader = PdfReader(os.path.join(ROOT_PATH, "uploads", path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size = 1024, chunk_overlap = 512)

docs = read_pdf("0d9c50ac-5c51-4b18-9524-59382ce2ce18.pdf")
doc_splits = text_splitter.split_text(docs)

vectorstore = Chroma.from_texts(
    texts=doc_splits,
    collection_name="rag-test-0d9c50ac-5c51-4b18-9524-59382ce2ce18",
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    'retrieve_cv',
    'Search and return information from uploaded CV'
)

tools = [retriever_tool]

def agent(state):
    print("---CALL AGENT---")
    messages = state["messages"]
    model = ChatOpenAI(temperature=0, streaming=True, model_name="gpt-3.5-turbo")
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": [response]}
    # return {"messages": []}

def generate(state):
    print("---GENERATE---")
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]

    docs = last_message.content

    prompt = hub.pull("rlm/rag-prompt")

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)

    rag_chain = prompt | llm | StrOutputParser()

    response = rag_chain.invoke({"context": docs, "question": question})
    return {"messages": [response]}

workflow = StateGraph(AgentState)

retrieve = ToolNode([retriever_tool])

workflow.add_node("agent", agent)
workflow.add_node("generate", generate)

workflow.add_edge(START, "agent")
workflow.add_edge("agent", "generate")
workflow.add_edge("generate", END)

graph = workflow.compile()

inputs = {
    "messages": [
        (
            "user",
            "What is Applicant's name?"
        )
    ]
}

for output in graph.stream(inputs):
    for key, value in output.items():
        pprint.pprint(f"Output from node '{key}':")
        pprint.pprint("---")
        pprint.pprint(value, indent=2, width=80, depth=None)
    pprint.pprint("\n--\n")

