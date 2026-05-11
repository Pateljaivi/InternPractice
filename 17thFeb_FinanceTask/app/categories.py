from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.database import categories, transactions, audit_logs, client
from app.schemas import CategoryCreate,CategoryUpdate

router = APIRouter()


@router.post("/")
async def create_category(data: CategoryCreate):
    doc = data.model_dump()
    doc["created_at"] = datetime.utcnow()
    await categories.insert_one(doc)
    return {"success": True}


@router.get("/")
async def list_categories():
    data = []
    async for cat in categories.find():
        cat["id"] = str(cat["_id"])
        del cat["_id"]
        data.append(cat)
    return {"success": True, "data": data}


@router.delete("/{name}")
async def delete_category(name: str):
    async with await client.start_session() as session:
        async with session.start_transaction():
            await categories.delete_one({"name": name})
            await transactions.update_many(
                {"category": name},
                {"$set": {"category": "uncategorized"}}
            )
            await audit_logs.insert_one({
                "action": "delete_category",
                "name": name,
                "timestamp": datetime.utcnow()
            })

    return {"success": True}

# @router.put("/{old_name}")
# async def update_category(old_name: str, data: CategoryUpdate):
#     async with await client.start_session() as session:
#         async with session.start_transaction():
#
#             existing = await categories.find_one({"name": old_name})
#             if not existing:
#                 raise HTTPException(status_code=404, detail="Category not found")
#
#             updated_data = data.model_dump(exclude_unset=True)
#
#             if not updated_data:
#                 raise HTTPException(status_code=400, detail="No updated data provided")
#
#             await categories.update_one({"name": old_name}, {"$set": updated_data})
#
#             if "name" in updated_data:
#                 await transactions.update_many(
#                     {"category": old_name},
#                     {"$set": {"category": updated_data["name"]}}
#                 )
#
#             await audit_logs.insert_one({
#                 "action": "update_category",
#                 "old_name": old_name,
#                 "new_name": updated_data.get("name"),
#                 "timestamp": datetime.utcnow()
#             })
#
#     return {"success": True,"message": "Category updated successfully"}


@router.patch("/{name}")
async def patch_category(name: str, data: CategoryUpdate):
    existing = await categories.find_one({"name": name})
    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")
    old_name = existing["name"]
    updated_data = data.model_dump(exclude_unset=True)

    if not updated_data:
        raise HTTPException(status_code=400, detail="No updated data provided")
    await categories.update_one({"name": name}, {"$set": updated_data})


    if "name" in updated_data:
        await transactions.update_many(
            {"category": old_name},
            {"$set": {"category": updated_data["name"]}}
        )
    log_data = {
        "action": "update_category",
        "old_name": old_name,
        "new_name": updated_data.get("name",old_name),
        "timestamp": datetime.utcnow()
    }
    result = await audit_logs.insert_one(log_data)


    return {"success": True, "message": "Category updated successfully","audit_id":str(result.inserted_id)}