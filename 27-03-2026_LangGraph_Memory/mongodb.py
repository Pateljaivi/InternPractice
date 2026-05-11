from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chat_memory"]
collection = db["messages"]

def save_message(user_id, message):
    collection.insert_one(
        {
            "user_id": user_id,
            "message": message
        }
    )

def get_messages(user_id):
    data = collection.find({"user_id": user_id})
    return [d["message"] for d in data]