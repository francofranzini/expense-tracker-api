from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.database import engine
from app import models
from app.routers import expenses, users
from app.limiter import limiter

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Expense Tracker API",
    swagger_ui_parameters={"persistAuthorization": True}
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(expenses.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API running"}
