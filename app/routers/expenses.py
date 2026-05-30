from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List

# Crea un router para poder redireccionar las llamadas a los endpoints correspondientes
router = APIRouter(prefix="/expenses", tags=["Expenses"])


# crea un endpoint en el router, de tipo post, con ExpenseResponse como esquema de salida
@router.post("/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


# Crea un endpoint en el router, de tipo get, con ExpenseResponse como esquema de salida
@router.get("/", response_model=List[schemas.ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()


@router.get("/summary", response_model=schemas.SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()

    count = len(expenses)
    total = sum(expense.amount for expense in expenses)
    average = total / count if count > 0 else 0

    return {"total": total, "count": count, "average": average}


@router.get("/summary/by-category", response_model=List[schemas.ByCategoryResponse])
def get_summary_by_category(db: Session = Depends(get_db)):
	categories = [c.value for c in models.CategoryEnum]
	tot = []
	for category in categories:
		expenses_category = db.query(models.Expense).filter(models.Expense.category == category).all()
		total_category = sum(expense.amount for expense in expenses_category)
		tot.append({"category": category, "total": total_category})
	return tot


# Crea un endpoint en el router, de tipo get, con Expense response como esquema de salida
# con un 'expense_id'. La primera linea que esta por encima de las funciones, se llama decorador
# crea una vinculacion entre router.get(...) y get_expense, donde la funcion contigua
# se ejecuta al ocurrir router.get(...)
@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


# Crea un endpoint de tipo put con Expense response como esquema de salida, con 'expense_id'
# Depends le dice a la funcion que necesita la conexion con la db antes de ejecutar la funcion
# data es completado por FastAPI con los datos del body. (y practicamente todo)
@router.put("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    expense_id: int, data: schemas.ExpenseUpdate, db: Session = Depends(get_db)
):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}
