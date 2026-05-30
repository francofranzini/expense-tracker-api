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
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)