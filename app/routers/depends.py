'''
Author: andy
Date: 2023-06-20 21:27:46
LastEditors: weijay
LastEditTime: 2023-07-11 18:45:39
Description: 依賴項目
'''


from fastapi import Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from app.database import SessionLocal, crud
from app.error_handle import CustomError
from app.schemas import auth_schema
from app.config.config import BaseConfig

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, BaseConfig.JWT_SECRET_KEY, algorithms=BaseConfig.JWT_ALGORITHM)
        username = payload.get("sub")

        if username is None:
            CustomError.credentials_execption()

        token_data = auth_schema.TokenData(username=username)

    except JWTError:
        CustomError.credentials_execption()

    user = crud.get_user_with_username(db, token_data.username)

    if user is None:
        CustomError.credentials_execption()

    return user
