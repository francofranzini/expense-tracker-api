import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func
from app.database import get_db
from app import models, schemas
from datetime import date
from typing import List, Optional
from app.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])
logger = logging.getLogger(__name__)


# crea un endpoint en el router, de tipo post, con ExpenseResponse como esquema de salida
@router.post("/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user) ):
    db_expense = models.Expense(**expense.model_dump(), user_id = user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    logger.info("Expense created: id=%s '%s' $%s (user %s)", db_expense.id, db_expense.title, db_expense.amount, user.id)
    return db_expense


# Crea un endpoint en el router, de tipo get, con ExpenseResponse como esquema de salida
@router.get("/", response_model=schemas.PaginatedExpenseResponse)
def get_expenses(
        category: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        db: Session = Depends(get_db),
        user: models.User = Depends(get_current_user)
    ):
    query = db.query(models.Expense).filter(models.Expense.user_id == user.id)

    if category:
        query = query.filter(models.Expense.category == category)
    if date_from:
        query = query.filter(models.Expense.created_at >= date_from)
    if date_to:
        query = query.filter(models.Expense.created_at <= date_to)

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total,
    }
        


@router.get("/summary", response_model=schemas.SummaryResponse)
def get_summary(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    result = db.query(
        sql_func.coalesce(sql_func.sum(models.Expense.amount), 0).label("total"),
        sql_func.count(models.Expense.id).label("count"),
        sql_func.coalesce(sql_func.avg(models.Expense.amount), 0).label("average"),
    ).filter(models.Expense.user_id == user.id).one()

    return {"total": result.total, "count": result.count, "average": result.average}


@router.get("/summary/by-category", response_model=List[schemas.ByCategoryResponse])
def get_summary_by_category(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    results = db.query(
        models.Expense.category,
        sql_func.coalesce(sql_func.sum(models.Expense.amount), 0).label("total"),
    ).filter(
        models.Expense.user_id == user.id
    ).group_by(models.Expense.category).all()

    totals_by_cat = {r.category: r.total for r in results}
    return [
        {"category": c.value, "total": totals_by_cat.get(c.value, 0)}
        for c in models.CategoryEnum
    ]


# Crea un endpoint en el router, de tipo get, con Expense response como esquema de salida
# con un 'expense_id'. La primera linea que esta por encima de las funciones, se llama decorador
# crea una vinculacion entre router.get(...) y get_expense, donde la funcion contigua
# se ejecuta al ocurrir router.get(...)
@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


# Crea un endpoint de tipo put con Expense response como esquema de salida, con 'expense_id'
# Depends le dice a la funcion que necesita la conexion con la db antes de ejecutar la funcion
# data es completado por FastAPI con los datos del body. (y practicamente todo)
@router.put("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int, data: schemas.ExpenseUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id , models.Expense.user_id == user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id , models.Expense.user_id == user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    logger.info("Expense deleted: id=%s (user %s)", expense_id, user.id)
    return {"message": "Expense deleted"}
