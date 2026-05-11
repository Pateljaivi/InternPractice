import streamlit as st

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage

from rag import data_store

import os
from dotenv import load_dotenv
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


llm = ChatOllama(
    model="mistral-nemo",
    base_url=BASE_URL
)
retriever = data_store.invoke({})

@tool
def retrieve_info(query: str):
    """
    Search this tool for ANY questions regarding:
    - PDF ingestion strategies, chunking, or RecursiveCharacterTextSplitter.
    - Company policies and FAQ from the uploaded PDFs.
    """
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])


st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("Intelligent RAG Based Chatbot")

system_message = (
                    "You are a professional assistant. "
                    "ALWAYS use the 'retrieve_info' tool to verify facts about PDF chunking"
                    "or project implementation before answering from your own memory."
)

agent = create_agent(
    model=llm,
    tools=[retrieve_info],
    system_prompt=system_message
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("Type your question...")
if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})


    response = agent.invoke({"messages": [HumanMessage(content=user_input)]})


    reply = response["messages"][-1].content


    st.session_state.messages.append({"role": "assistant", "content": reply})


    st.rerun()


