'''
Author: andy
Date: 2023-06-20 02:30:07
LastEditors: weijay
LastEditTime: 2023-07-19 01:36:52
Description: 使用者路由，這些 api 需要通過認證後才能存取
'''

from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import auth
from app.schemas import user_schema, database_schema, auth_schema, restaurant_schema
from app.database import crud, model
from app.routers.depends import get_db, get_current_user
from app.error_handle import ErrorHandler
from app.utils import MapApi


router = APIRouter(prefix="/user")


@router.post("/token", response_model=auth_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """使用者登入,會回傳一個 access token """

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
    """使用者註冊"""
    
    user = crud.get_user_with_username(db, items.username)

    if user:
        raise HTTPException(409, "username or email is exist.")

    user = crud.get_user_with_email(db, items.email)

    if user:
        raise HTTPException(409, "username or email is exist.")

    crud.create_user_not_oauth(db, database_schema.UserNotOAuthDBModel(**items.dict()))

    return {"message": "created."}


@router.get("/restaurant", response_model=restaurant_schema.OnReadsModel)
def read_user_restaurants(
    db: Session = Depends(get_db), user: model.User = Depends(get_current_user)
):
    """取得使用者儲存的所有餐廳 (需要使用者登入)"""

    items = crud.get_restaurants_with_user(db, user.id)

    return restaurant_schema.OnReadsModel(items=items)


@router.post("/restaurant", status_code=201)
def create_user_restaurant(
    items: restaurant_schema.OnCreateModel,
    db: Session = Depends(get_db),
    user: model.User = Depends(get_current_user),
):
    """使用者新增餐廳"""

    # 檢查傳入的 open_time 中的 time 格式
    if items.open_times is not None:
        for open_time in items.open_times:
            try:
                datetime.strptime(open_time.open_time, "%H:%M").time()
                datetime.strptime(open_time.close_time, "%H:%M").time()

            except ValueError:
                ErrorHandler.raise_400("time format error, it should be %H:%M format.")

    # 使用第三方 Api 取得經緯度
    lat, lng = MapApi().get_coords(items.address)

    full_item = database_schema.RestaurantDBModel(**items.dict(), lat=lat, lng=lng)

    if not (lat and lng):
        ErrorHandler.raise_400(
            f"The address '{items.address}' format is incorrect and cannot be processed correctly."
        )

    r = crud.create_restaurant_with_user(db, full_item, user.id)

    if items.open_times is not None:
        db_open_times = []

        for open_time_obj in items.open_times:
            db_open_times.append(
                database_schema.RestaurantOpenTimeDBModel(
                    day_of_week=open_time_obj.day_of_week,
                    close_time=datetime.strptime(open_time_obj.close_time, "%H:%M").time(),
                    open_time=datetime.strptime(open_time_obj.open_time, "%H:%M").time(),
                )
            )

        crud.create_restaurant_open_times(db, r.id, db_open_times)

    return {"message": "created."}


@router.patch("/restaurant/{restaurant_id}")
def update_user_restaurant(
    restaurant_id: int,
    item: restaurant_schema.OnUpdateModel,
    db: Session = Depends(get_db),
    user: model.User = Depends(get_current_user),
):
    """更新使用者餐廳資料"""

    # 身份確認
    if not crud.check_is_user_restaurant(db, user.id, restaurant_id):
        raise HTTPException(403)

    updated_restaurant = crud.update_restaurant(
        db, restaurant_id, database_schema.RestaurantUpdateDBModel(**item.dict())
    )

    if not updated_restaurant:
        ErrorHandler.raise_404(f"The restaurant ID: {restaurant_id} is not founded in database.")

    return {"message": "ok"}


@router.delete("/restaurant/{restaurant_id}")
def delete_user_restaurant(
    restaurant_id: int, db: Session = Depends(get_db), user: model.User = Depends(get_current_user)
):
    """刪除使用者指定 ID 餐廳"""

    if not crud.check_is_user_restaurant(db, user.id, restaurant_id):
        raise HTTPException(403)

    deleted_restaurant = crud.delete_restaurant(db, restaurant_id)

    if not deleted_restaurant:
        ErrorHandler.raise_404(f"The restaurant ID: {restaurant_id} is not founded in database.")

    return {"message": f"Restaurant ID {deleted_restaurant.id} has been deleted."}


@router.post("/restaurant/{restaurant_id}/open_time", status_code=201)
def create_user_restaurant_open_time(
    restaurant_id: int,
    open_times: restaurant_schema.OnCreateOpenTimeModel,
    db: Session = Depends(get_db),
    user: model.User = Depends(get_current_user),
):
    """更新使用者指定 ID 餐廳"""

    if not crud.check_is_user_restaurant(db, user.id, restaurant_id):
        raise HTTPException(403)

    open_times_obj = [
        database_schema.RestaurantOpenTimeDBModel(**open_time.dict())
        for open_time in open_times.items
    ]

    crud.create_restaurant_open_times(db, restaurant_id, open_times_obj)

    return {"message": "created."}


@router.patch("/restaurant/{restaurant_id}/open_time/{open_time_id}")
def update_user_restaurant_open_time(
    restaurant_id: int,
    open_time_id: int,
    item: restaurant_schema.OnUpadteOpenTimeModel,
    db: Session = Depends(get_db),
    user: model.User = Depends(get_current_user),
):
    """更新使用者指定餐廳 ID 營業時間"""

    if not crud.check_is_user_restaurant(db, user.id, restaurant_id):
        raise HTTPException(403)

    updated_open_time = crud.update_restaurant_open_time(
        db, open_time_id, database_schema.RestaurantOpenTimeUpdateDBModel(**item.dict())
    )

    if not updated_open_time:
        ErrorHandler.raise_404(f"The open time ID: {open_time_id} is not founded in database.")

    return {"message": "updated."}


@router.delete("/restaurant/{restaurant_id}/open_time/{open_time_id}")
def delete_user_restaurant_open_time(
    restaurant_id: int,
    open_time_id: int,
    db: Session = Depends(get_db),
    user: model.User = Depends(get_current_user),
):
    """刪除使用者指定 ID 餐廳營業時間"""

    if not crud.check_is_user_restaurant(db, user.id, restaurant_id):
        raise HTTPException(403)

    deleted_open_time = crud.delete_restaurant_open_time(db, open_time_id)

    if deleted_open_time is None:
        ErrorHandler.raise_404(f"The open time ID: {open_time_id} is not founed in database.")

    return {"message": f"Open time ID: {open_time_id} has been deleted."}
