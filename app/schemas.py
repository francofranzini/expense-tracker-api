from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models import CategoryEnum


class ExpenseCreate(BaseModel):
    title: str
    amount: Decimal
    category: CategoryEnum
    description: Optional[str] = None


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[Decimal] = None
    category: Optional[CategoryEnum] = None
    description: Optional[str] = None


class ExpenseResponse(BaseModel):
    id:          int
    title:       str
    amount:      Decimal
    category:    str
    description: Optional[str]
    created_at:  datetime
    user_id:     int

    model_config = ConfigDict(from_attributes=True)

class PaginatedExpenseResponse(BaseModel):
    items: List[ExpenseResponse]
    total: int
    skip: int
    limit: int
    has_more: bool


class SummaryResponse(BaseModel):
    total: Decimal
    count: int
    average: Decimal


class ByCategoryResponse(BaseModel):
    category: str
    total: Decimal

class TopCategoryResponse(BaseModel):
    category: str
    total: Decimal

class UserCreate(BaseModel):
    username: str
    password: str
class UserLogin(BaseModel):
    username: str
    password: str
class UserResponse(BaseModel):
    id:         int
    username:   str

    model_config = ConfigDict(from_attributes=True)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str  # siempre va a ser "bearer"