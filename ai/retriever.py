import os.path
from pypdf import PdfReader

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

def read_pdf(path: str):
    reader = PdfReader(os.path.join(ROOT_PATH, "uploads", path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size = 128, chunk_overlap = 16)

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

def get_retriever_tool():
    return retriever_tool