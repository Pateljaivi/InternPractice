from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage

from RAG import store_data
from DATABASE import memory,summarization_middleware

from dotenv import load_dotenv
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


llm = ChatOllama(
    model = "mistral-nemo",
    base_url=BASE_URL
)
retriever = store_data.invoke({})

@tool
def retrieve_info(query:str):
    """
        Search this tool for ANY questions regarding:
        - PDF ingestion strategies, chunking, or RecursiveCharacterTextSplitter.
        - How MongoDB persistence is implemented in THIS specific project.
        - Company policies and FAQ from the uploaded PDFs.
    """
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])


def state_modifier(state):
    return summarization_middleware.invoke(state["messages"])


def chat():
    print("--- RAG Agent (MongoDB & Summarization Active) ---")

    system_message = ("You are a professional assistant. "
                      "ALWAYS use the 'retrieve_info' tool to verify facts about PDF chunking"
                      "or project implementation before answering from your own memory.")

    agent = create_agent(
        model=llm,
        tools=[retrieve_info],
        checkpointer=memory,
        system_prompt=system_message
    )

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        config = {"configurable": {"thread_id": "user825"}}


        response = agent.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )

        print("AI:", response["messages"][-1].content)


if __name__ == "__main__":
    chat()