from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from passlib.context import CryptContext
from app import models, schemas
from typing import List
from app.auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

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

@router.post("/login", response_model = schemas.TokenResponse)
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
	if not db_user:
		raise HTTPException(status_code=401, detail="User not found")
	if not pwd_context.verify(form_data.password, db_user.password):
		#incorrect password
		raise HTTPException(status_code=400, detail="Incorrect password")
	#create token
	token = create_access_token(data={"sub": db_user.username})
	return {"access_token": token, "token_type": "bearer"}