from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import os
from jose import jwt
from datetime import datetime, timedelta
SECRET_PASSKEY = os.getenv("SECRET_PASSKEY")

SECRET_KEY = SECRET_PASSKEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7200

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #(junta sub+exp en base 64 y le agrega la firma)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
#(token = sub.exp.signature) 
#jwt decode verifica la firma, la expiracion 
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username = payload.get("sub")
		if username is None:
			raise HTTPException(status_code=401, detail="Invalid token")
	except:
		raise HTTPException(status_code=401, detail="Invalid token")

	user = db.query(models.User).filter(models.User.username == username).first()
	if user is None:
		raise HTTPException(status_code=401, detail="Invalid token")
	return user