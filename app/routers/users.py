import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from passlib.context import CryptContext
from app import models, schemas
from typing import List
from app.auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.limiter import limiter

router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
logger = logging.getLogger(__name__)


@router.post("/create", response_model = schemas.UserResponse)
@limiter.limit("5/minute")
def user_create(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
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
	logger.info("User registered: '%s'", db_user.username)
	return db_user

@router.post("/login", response_model = schemas.TokenResponse)
@limiter.limit("10/minute")
def user_login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
	if not db_user:
		logger.warning("Failed login — user not found: '%s'", form_data.username)
		raise HTTPException(status_code=401, detail="User not found")
	if not pwd_context.verify(form_data.password, db_user.password):
		logger.warning("Failed login — wrong password for user: '%s'", form_data.username)
		raise HTTPException(status_code=400, detail="Incorrect password")
	token = create_access_token(data={"sub": db_user.username})
	logger.info("User logged in: '%s'", db_user.username)
	return {"access_token": token, "token_type": "bearer"}