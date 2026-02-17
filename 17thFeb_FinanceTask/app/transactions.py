from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime,timezone
from app.database import transactions
from app.schemas import TransactionCreate
from app.dependencies import pagination
from app.utils import serialize, validate_id

router = APIRouter()


@router.post("/")
async def create_tx(data: TransactionCreate):
    tx = data.model_dump()
    tx["created_at"] = datetime.utcnow()
    tx["updated_at"] = datetime.utcnow()

    result = await transactions.insert_one(tx)
    new_tx = await transactions.find_one({"_id": result.inserted_id})

    return {"success": True, "data": serialize(new_tx)}


@router.get("/")
async def list_tx(
    category: str | None = None,
    type: str | None = None,
    from_date: str | None = Query(None, alias="from"),
    to_date: str | None = Query(None, alias="to"),
    tags: list[str] | None = Query(None),
    sort_by: str = "date",
    order: str = "desc",
    page_data=Depends(pagination)
):
    query = {}

    if category:
        query["category"] = category.lower()

    if type:
        query["type"] = type

    if from_date or to_date:
        query["date"] = {}
        if from_date:
            query["date"]["$gte"] = datetime.fromisoformat(from_date)
        if to_date:
            query["date"]["$lte"] = datetime.fromisoformat(to_date)

    if tags:
        query["tags"] = {"$all": tags}

    skip = (page_data.page - 1) * page_data.page_size
    sort_order = -1 if order == "desc" else 1

    cursor = transactions.find(query)\
        .sort(sort_by, sort_order)\
        .skip(skip)\
        .limit(page_data.page_size)

    data = [serialize(tx) async for tx in cursor]

    return {"success": True, "data": data}


@router.get("/search")
async def search(q: str):
    cursor = transactions.find({"$text": {"$search": q}})
    return {"success": True, "data": [serialize(tx) async for tx in cursor]}


@router.get("/summary")
async def summary(month: str):
    # 1. Parse and make dates "Aware"
    year, m = map(int, month.split("-"))
    start = datetime(year, m, 1, tzinfo=timezone.utc)

    if m == 12:
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(year, m + 1, 1, tzinfo=timezone.utc)

    # 2. Build the Pipeline
    pipeline = [
        {"$match": {"date": {"$gte": start, "$lt": end}}},
        {
            "$facet": {
                "totals": [
                    {"$group": {"_id": "$type", "total": {"$sum": "$amount"}}}
                ],
                "category_breakdown": [
                    {"$match": {"type": "expense"}},
                    {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}
                ],
                "highest_expense": [
                    {"$match": {"type": "expense"}},
                    {"$sort": {"amount": -1}},
                    {"$limit": 1}
                ]
            }
        }
    ]

    result = await transactions.aggregate(pipeline).to_list(1)

    if not result:
        return {"success": True, "data": {}}

    data = result[0]

    # Convert ObjectId to string in highest_expense if it exists
    if data.get("highest_expense"):
        for item in data["highest_expense"]:
            item["_id"] = str(item["_id"])

    return {"success": True, "data": data}



@router.delete("/bulk")
async def bulk_delete(
    category: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None
):
    query = {}

    if category:
        query["category"] = category.lower()

    if from_date or to_date:
        query["date"] = {}
        if from_date:
            query["date"]["$gte"] = datetime.fromisoformat(from_date)
        if to_date:
            query["date"]["$lte"] = datetime.fromisoformat(to_date)

    result = await transactions.delete_many(query)

    return {"success": True, "deleted": result.deleted_count}


@router.get("{tx_id}")
async def get_tx(tx_id: str):

    obj_id = validate_id(tx_id)

    tx = await transactions.find_one({"_id": obj_id})

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {"success": True, "data": serialize(tx)}

@router.put("/{tx_id}")
async def update_tx(tx_id: str,data: TransactionCreate):

    obj_id = validate_id(tx_id)

    existing = await transactions.find_one({"_id": obj_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Transaction not found")

    update_data = data.model_dump()
    update_data["updated_at"] = datetime.utcnow()

    await transactions.update_one({"_id": obj_id}, {"$set": update_data})

    updated = await transactions.find_one({"_id": obj_id})

    return {"success": True, "data": serialize(updated)}

@router.delete("/{tx_id}")
async def delete_tx(tx_id: str):
    obj_id = validate_id(tx_id)

    result = await transactions.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"success": True,"message": "Transaction successfully deleted"}