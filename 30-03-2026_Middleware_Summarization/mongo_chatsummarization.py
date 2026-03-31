import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_mongodb import MongoDBChatMessageHistory
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()


MONGO_URI = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
MODEL = os.getenv("LLAMA_MODEL", "llama3.2:1b")


llm = ChatOllama(
    model=MODEL,
    temperature=0,
    base_url="http://127.0.0.1:11434",
    timeout=120
)


mongo_memory = MongoDBChatMessageHistory(
    connection_string=MONGO_URI,
    session_id="user_simple_session",
    database_name="middleware_db",
    collection_name="history"
)

checkpointer = MemorySaver()



agent = create_agent(
    model=llm,
    checkpointer=checkpointer,
    system_prompt="You are a helpful assistant. Use 'Old info' to help the user.",
    middleware=[
        SummarizationMiddleware(
            model=llm,
            model_provider="ollama",
            trigger=("messages", 6),
            keep=("messages", 4)
        )
    ]
)


def get_old_context(query):

    for m in reversed(mongo_memory.messages):
        if query.lower() in m.content.lower():
            return m.content
    return ""


print("\n--- Chat started! (Type 'exit' to stop) ---")
config = {"configurable": {"thread_id": "thread_primary"}}

while True:
    user_input = input("\nUser: ").strip()
    if user_input.lower() in ["exit", "quit", "bye"]:
        break
    if not user_input:
        continue


    old_info = get_old_context(user_input)


    if old_info:
        enhanced_query = f"Old info: {old_info}\n\nUser Question: {user_input}"
    else:
        enhanced_query = user_input

    try:

        result = agent.invoke(
            {"messages": [HumanMessage(content=enhanced_query)]},
            config=config
        )

        reply = result["messages"][-1].content
        print(f"AI: {reply}")

        mongo_memory.add_user_message(user_input)
        mongo_memory.add_ai_message(reply)

    except Exception as e:
        print(f"Error: {e}. Make sure Ollama is running (ollama serve).")

print("\nGoodbye! Session history is safely stored in MongoDB.")


