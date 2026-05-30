from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExpenseCreate(BaseModel):
    title:        str
    amount:       float
    category:     str
    description:  Optional[str] = None

class ExpenseUpdate(BaseModel):
    title:       Optional[str] = None
    amount:      Optional[float] = None
    category:    Optional[str] = None
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id:           int
    title:        str
    amount:       float
    category:     str
    description:  Optional[str]
    created_at:   datetime

    class Config:
        from_attributes = True