from fastapi import FastAPI
from app.database import create_indexes
from app.transactions import router as transaction_router
from app.categories import router as category_router

app = FastAPI(title="Personal Finance Tracker API")

app.include_router(transaction_router, prefix="/transactions", tags=["Transactions"])
app.include_router(category_router, prefix="/categories", tags=["Categories"])


@app.on_event("startup")
async def startup():
    await create_indexes()