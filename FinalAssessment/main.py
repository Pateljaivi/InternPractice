from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.chat_models import ChatOllama
from rag import get_retriever
from database import *

embedding = OllamaEmbeddings(
        model = "nomic-embed-text",
        base_url=BASE_URL
    )
vector_store = InMemoryVectorStore(embedding)

llm = ChatOllama(model="mistral-nemo", base_url="http://172.16.1.224:11434")

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

def chat():

    print("RAG Based chatbot...")


    agent = create_agent(
        model = llm,
        tools=[retrieve_context],
        # checkpointer=memory
    )

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        config = {"configurable": {"thread_id": "user_id"}}
        response = agent.invoke(
            {"messages": [("user", query)]},
            config=config
        )
        print(response)
        print("AI:", response["messages"][-1].content)


if __name__ == "__main__":
    chat()