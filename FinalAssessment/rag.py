from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from FinalAssessment.database import BASE_URL


@tool()
def get_retriever():
    """
    It parse the document and store chunks,embedding in chromaDB
    """
    all_docs = []

    files = [
        "data/company_policies.pdf",
        "data/faq.pdf",
        "data/product_manual.pdf",
    ]

    for file in files:
        docs = PyPDFLoader(file)
        loader = docs.load()
        all_docs.extend(loader)


    text_split = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100,
    )
    chunks = text_split.split_documents(all_docs)
    embedding = OllamaEmbeddings(
        model = "nomic-embed-text",
        base_url=BASE_URL
    )
    vector_store = InMemoryVectorStore(embedding)

    document_ids = vector_store.add_documents(documents=chunks)

    print(document_ids[:3])

if __name__ == "__main__":
    get_retriever()




