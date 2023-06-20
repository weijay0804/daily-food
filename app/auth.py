'''
Author: andy
Date: 2023-06-20 22:22:09
LastEditors: andy
LastEditTime: 2023-06-20 23:49:25
Description: 存放跟使用者認證相關的程式
'''

from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from jose import jwt

from app.config.config import BaseConfig
from app.database import crud
from app.schemas.user_schema import OnReadNoOAuthModel


def authenticate_user(db: Session, username: str, password: str) -> "OnReadNoOAuthModel":
    """認證使用者

    如果認證通過則回傳對應的物件，反之回傳 `False`
    """

    user = crud.get_user_not_oauth(db, username)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return OnReadNoOAuthModel(id=user.id, username=user.username, email=user.email)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """生成 JWT Token
    `expires_delta` 默認值為 15 min
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, BaseConfig.JWT_SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM
    )

    return encoded_jwt
