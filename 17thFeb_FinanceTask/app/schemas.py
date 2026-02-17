from pydantic import BaseModel, Field, field_validator
from datetime import datetime,timezone
from typing import List, Optional


class TransactionCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    amount: float = Field(gt=0)
    type: str
    category: str
    date: datetime
    tags: List[str] = []

    @field_validator("title")
    def strip_title(cls, v):
        return v.strip()

    @field_validator("type")
    def validate_type(cls, v):
        if v not in ["income", "expense"]:
            raise ValueError("Type must be income or expense")
        return v

    @field_validator("category")
    def validate_category(cls, v):
        if not v.strip():
            raise ValueError("Category required")
        return v.lower()

    @field_validator("date")
    def no_future(cls, v):
        if v > datetime.now(timezone.utc):
            raise ValueError("Future date not allowed")
        return v

    @field_validator("tags")
    def validate_tags(cls, v):
        if len(v) > 10:
            raise ValueError("Max 10 tags allowed")
        for tag in v:
            if len(tag) > 30:
                raise ValueError("Tag too long")
        return v


class CategoryCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None

    @field_validator("name")
    def lower_name(cls, v):
        return v.strip().lower()

    @field_validator("type")
    def validate_type(cls, v):
        if v not in ["income", "expense", "both"]:
            raise ValueError("Invalid category type")
        return v

class CategoryUpdate(BaseModel):
    name: Optional[str] = None