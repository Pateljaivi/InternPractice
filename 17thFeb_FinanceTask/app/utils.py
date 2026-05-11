from bson import ObjectId
from fastapi import HTTPException


def serialize(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


def validate_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    return ObjectId(id)