import json
import operator
import os
from typing import Annotated, List, TypedDict

from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langgraph.graph import END, StateGraph, START
from langgraph.types import Send

class CvState(TypedDict):
    questions: list
    context: str
    intermediate_answers: Annotated[list, operator.add]
    final_answer: str

class QuestionState(TypedDict):
    question: str
    context: str

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

llm = ChatOpenAI(temperature=0, streaming=True, model_name="gpt-3.5-turbo")
embeddings = OpenAIEmbeddings()

def load_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    return vectorstore

def answer_questions(state: CvState):
    return [Send("question", {"question": question, "context": state["context"]}) for question in state["questions"]]

def question_function(state: QuestionState):
    question = state["question"]
    context = state["context"]

    prompt = hub.pull("rlm/rag-prompt")

    formatted_prompt = prompt.format(context=context, question=question)

    response = llm.invoke(formatted_prompt)

    return {"intermediate_answers": [json.dumps({"question": question, "answer": response.content})]}

def recap_function(state: CvState):
    return {"final_answer": "\n--\n".join(state["intermediate_answers"])}

def create_rag_graph():
    workflow = StateGraph(CvState)

    workflow.add_node("question", question_function)
    workflow.add_node("recap", recap_function)

    workflow.add_conditional_edges(START, answer_questions, ["question"])
    workflow.add_edge("question", "recap")
    workflow.add_edge("recap", END)

    return workflow.compile()

def analyze_cv(pdf_path: str, questions: List[str]):
    vectorstore = load_pdf(pdf_path)

    context = " ".join([doc.page_content for doc in vectorstore.similarity_search("")])

    state = CvState(
        context=context,
        questions=questions,
        intermediate_answers=[],
        final_answer=""
    )

    graph = create_rag_graph()
    result = graph.invoke(state)

    return result["final_answer"]

if __name__ == "__main__":
    pdf_path = os.path.join(ROOT_PATH, "uploads", "0d9c50ac-5c51-4b18-9524-59382ce2ce18.pdf")
    questions = [
        "What is applicant's name?",
        "Give me a link to the applicant's LinkedIn profile",
    ]

    result = analyze_cv(pdf_path, questions)
    print(result)
