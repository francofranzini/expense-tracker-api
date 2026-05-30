from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from passlib.context import CryptContext
from app import models, schemas
from typing import List

# Crea un router para poder redireccionar las llamadas a los endpoints correspondientes
router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


@router.post("/create", response_model = schemas.UserResponse)
def user_create(user: schemas.UserCreate, db: Session = Depends(get_db)):
	db_user = models.User(**user.model_dump())
	#We verify that no user with the same name exists
	repeated = db.query(models.User).filter(models.User.username == db_user.username).first()
	if(repeated):
		raise HTTPException(status_code=400, detail="Username already exists")
	#Debemos hashear su contraseña
	db_user.password = pwd_context.hash(db_user.password) 
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user