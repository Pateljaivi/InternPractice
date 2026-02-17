import motor.motor_asyncio
from pymongo import ASCENDING, DESCENDING, TEXT

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.finance_db

transactions = db.transactions
categories = db.categories
audit_logs = db.audit_logs


async def create_indexes():
    await transactions.create_index([("date", DESCENDING)])
    await transactions.create_index([("category", ASCENDING), ("date", DESCENDING)])
    await transactions.create_index([("type", ASCENDING), ("date", DESCENDING)])
    await transactions.create_index([("title", TEXT), ("description", TEXT)])
    await categories.create_index("name", unique=True)