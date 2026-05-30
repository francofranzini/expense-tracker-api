from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models import CategoryEnum


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: CategoryEnum
    description: Optional[str] = None


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[CategoryEnum] = None
    description: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SummaryResponse(BaseModel):
    total: float
    count: int
    average: float


class ByCategoryResponse(BaseModel):
    category: str
    total: float

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id:         int
    username:   str

    class Config:
        from_attributes = True
class TokenResponse(BaseModel):
    access_token: str
    token_type: str  # siempre va a ser "bearer"