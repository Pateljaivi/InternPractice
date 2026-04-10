import os
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver

from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("BASE_URL")
client = MongoClient("mongodb://localhost:27017/")
db = client["Chats"]
collection = db["Messages"]

memory = MongoDBSaver(client, db_name="chat_checkpoints")



