from datetime import datetime
from typing import List


class TransactionModel:
    _id: str
    title: str
    description: str
    amount: float
    type: str
    category: str
    date: datetime
    tags: List[str]
    created_at: datetime
    updated_at: datetime


class CategoryModel:
    _id: str
    name: str
    type: str
    description: str
    created_at: datetime