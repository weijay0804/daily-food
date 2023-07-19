'''
Author: andy
Date: 2023-06-20 02:30:07
LastEditors: weijay
LastEditTime: 2023-07-06 23:57:57
Description: 使用者路由
'''

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import auth
from app.schemas import user_schema, database_schema, auth_schema
from app.database import crud
from app.routers.depends import get_db, get_current_user


router = APIRouter(prefix="/user")


@router.post("/token", response_model=auth_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=15)
    acess_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": acess_token, "token_type": "bearer"}


@router.post("/", status_code=201)
def register(items: user_schema.OnCreateNoOAuthModel, db: Session = Depends(get_db)):
    user = crud.get_user_with_username(db, items.username)

    if user:
        raise HTTPException(409, "username or email is exist.")

    user = crud.get_user_with_email(db, items.email)

    if user:
        raise HTTPException(409, "username or email is exist.")

    crud.create_user_not_oauth(db, database_schema.UserNotOAuthDBModel(**items.dict()))

    return {"message": "created."}
