import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import tool
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from pypdf.errors import PdfStreamError

load_dotenv()
BASE_URL=os.getenv("BASE_URL")

@tool
def data_store():
    """This Function process the documents and store chunks with embeddings..."""


    all_docs = []

    files = [
        "data/company_policies.pdf",
        "data/faq.pdf",
        "data/product_manual.pdf",
    ]

    for file in files:
        try:
            loader = PyPDFLoader(file)
            docs = loader.load()
            all_docs.extend(docs)
        except PdfStreamError:
            print(f"Skipping corrupted PDF: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")


    text_split = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunk = text_split.split_documents(all_docs)

    embeddings = OllamaEmbeddings(
        model = "nomic-embed-text",
        base_url=BASE_URL
    )

    vectors = Chroma.from_documents(
        chunk,
        embeddings,
        persist_directory="./chroma1_db"
    )
    # print(f"Loaded {len(chunk)} chunks into Chroma")

    return vectors.as_retriever(search_kwargs={"k":3})


