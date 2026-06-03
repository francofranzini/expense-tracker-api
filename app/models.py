from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum


class CategoryEnum(str, Enum):
    food = "food"
    transport = "transport"
    operations = "operations"
    utilities = "utilities"
    entertainment = "entertainment"
    other = "other"


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

class User(Base):
    __tablename__ = "users"
    id =        Column(Integer, primary_key=True, index=True)
    username =  Column(String, nullable=False, unique=True)
    password =  Column(String, nullable=False)
