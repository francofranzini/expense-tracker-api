from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import expenses, users

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Expense Tracker API",
    swagger_ui_parameters={"persistAuthorization": True}
)
app.include_router(expenses.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API running"}
