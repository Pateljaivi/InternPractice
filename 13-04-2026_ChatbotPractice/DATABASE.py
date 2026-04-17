import os
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain_ollama import ChatOllama
from langchain.agents.middleware.summarization import SummarizationMiddleware
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


#MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

memory = MongoDBSaver(client, db_name="chatbot_checkpoints")

summary_llm = ChatOllama(
    model="llama3.2:latest",
    base_url=BASE_URL
)

#Summarization Middleware
summarization_middleware = SummarizationMiddleware(
    model=summary_llm,
    trigger=("messages",6),
    keep=("messages",2)
)

#When you use MongoDBSaver, the program follows this cycle:
#Before responding: The agent looks into MongoDB for a thread_id (a unique ID for your chat session).
#It "loads" the last checkpoint to remember what happened before.
#During processing: As the agent works, it updates the state.
#After responding: The agent takes a "snapshot" of the new state and writes it back to MongoDB as a new checkpoint.



#CHECKPOINT->A checkpoint captures the entire State of your chatbot after every interaction. This includes:
#The Message History: Every word said by the user and the AI.
#Internal Variables: Any data the agent is holding (like retrieved context from your PDFs).
#The Progress: Where the agent is in its "thought process".







