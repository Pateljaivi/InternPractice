import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

@tool()
def store_data():
    """This Function process the documents and store chunks with embeddings..."""

    all_docs = []

    files = [
        "data/company_policies.pdf",
        "data/faq.pdf",
        "data/product_manual.pdf"
    ]

    for file in files:
        docs = PyPDFLoader(file)
        loader = docs.load()
        all_docs.extend(loader)

    text_split = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_split.split_documents(all_docs)


    embedding = OllamaEmbeddings(
        model = "nomic-embed-text",
        base_url=BASE_URL
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="./my_chroma_db"
    )

    print("Data stored in ChromaDB!!!")

    return vector_store.as_retriever(search_kwargs={"k":3})