from pwdlib import PasswordHash
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
password_hash = PasswordHash.recommended()
from datetime import datetime, timezone, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import database
from sqlalchemy.orm import Session
import models

def hashed_password(password:str):
    return password_hash.hash(password)

def verify_password(plainpassword:str, hashpassword:str):
    return password_hash.verify(plainpassword, hashpassword)

def create_access_toekn(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, ALGORITHM )
    return encoded_jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/admin/login')



def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    admin = db.query(models.Admin).filter(
        models.Admin.username == username
    ).first()

    if admin is None:
        raise credentials_exception

    return admin
