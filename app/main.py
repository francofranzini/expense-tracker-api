from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import expenses

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(expenses.router)


@app.get("/")
def root():
    return {"message": "Expense Tracker API running"}
