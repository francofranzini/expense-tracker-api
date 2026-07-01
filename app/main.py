import logging
import time
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.database import engine
from app import models
from app.routers import expenses, users
from app.limiter import limiter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Expense Tracker API",
    swagger_ui_parameters={"persistAuthorization": True}
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(expenses.router)
app.include_router(users.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logging.getLogger("api.requests").info(
        "%s %s → %s (%.1fms)", request.method, request.url.path, response.status_code, duration_ms
    )
    return response


@app.get("/")
def root():
    return {"message": "Expense Tracker API running"}
