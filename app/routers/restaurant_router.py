'''
Author: weijay
Date: 2023-04-24 15:58:18
LastEditors: weijay
LastEditTime: 2023-07-19 01:43:00
Description: 餐廳路由
'''

from datetime import datetime
from typing import Union

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas import restaurant_schema, database_schema
from app.database import crud
from app.utils import MapApi
from app.error_handle import ErrorHandler
from app.routers.depends import get_db


router = APIRouter(prefix="/restaurant")


@router.get("/", response_model=restaurant_schema.OnReadsModel)
def read_restaurants(db: Session = Depends(get_db)):
    """取得所有餐廳列表"""

    items = crud.get_restaurants(db)

    return restaurant_schema.OnReadsModel(items=items)


@router.post("/", status_code=201)
def create_restaurant(items: restaurant_schema.OnCreateModel, db: Session = Depends(get_db)):
    """新增一個餐廳資料"""

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

    r = crud.create_restaurant(db, full_item)

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


@router.patch("/{restaurant_id}", status_code=200)
def update_restaurant(
    restaurant_id: str, item: restaurant_schema.OnUpdateModel, db: Session = Depends(get_db)
):
    """更新指定 ID 的的餐廳資料"""

    # TODO 這裡要檢查有沒有更改到 `address` ，如果有，要重新取得經緯度

    updated_restaurant = crud.update_restaurant(
        db, restaurant_id, database_schema.RestaurantUpdateDBModel(**item.dict())
    )

    if not updated_restaurant:
        ErrorHandler.raise_404(f"The restaurant ID: {restaurant_id} is not founded in database.")

    return {"message": "updated."}


@router.delete("/{restaurant_id}", status_code=200)
def delete_restaurant(restaurant_id: str, db: Session = Depends(get_db)):
    """刪除指定 ID 的餐廳資料"""

    deleted_restaurant = crud.delete_restaurant(db, restaurant_id)

    if not deleted_restaurant:
        ErrorHandler.raise_404(f"The restaurant ID: {restaurant_id} is not founded in database.")

    return {"message": f"Restaurant ID {deleted_restaurant.id} has been deleted."}


@router.post("/{restaurant_id}/open_time", status_code=201)
def create_restaurnt_open_time(
    restaurant_id: int,
    open_times: restaurant_schema.OnCreateOpenTimeModel,
    db: Session = Depends(get_db),
):
    """建立一個指定 ID 的餐聽營業時間"""

    open_times_obj = [
        database_schema.RestaurantOpenTimeDBModel(**open_time.dict())
        for open_time in open_times.items
    ]

    crud.create_restaurant_open_times(db, restaurant_id, open_times_obj)

    return {"message": "created."}


@router.patch(
    "/open_time/{open_time_id}",
    status_code=200,
)
def update_restauarnt_open_time(
    open_time_id: int,
    item: restaurant_schema.OnUpadteOpenTimeModel,
    db: Session = Depends(get_db),
):
    """更新一個指定 ID 的餐廳營業時間"""

    db_update_obj = database_schema.RestaurantOpenTimeUpdateDBModel(**item.dict(exclude_unset=True))
    updated_open_time = crud.update_restaurant_open_time(db, open_time_id, db_update_obj)

    if not updated_open_time:
        ErrorHandler.raise_404(f"The open time ID: {open_time_id} is not founded in database.")

    return {"message": "updated."}


@router.delete("/open_time/{open_time_id}", status_code=200)
def delete_restaurant_open_time(open_time_id: int, db: Session = Depends(get_db)):
    """刪除一個指定 ID 的餐廳營業時間"""

    deleted_open_time = crud.delete_restaurant_open_time(db, open_time_id)

    if not deleted_open_time:
        ErrorHandler.raise_404(f"The open time ID: {open_time_id} is not founed in database.")

    return {"message": f"Open time ID: {open_time_id} has been deleted."}


# TODO 這個要複製一份到 `../user_router.py` 中
# 在 `../user_rotuer.py` 中的，只會推薦給使用者儲存的餐廳
@router.get("/choice", response_model=restaurant_schema.OnReadsModel)
def read_restaurant_randomly(
    lat: float = Query(default=..., description="所在位置的緯度值"),
    lng: float = Query(default=..., description="所在位置的經度值"),
    distance: float = Query(default=..., description="要查詢多少距離範圍內 (km)"),
    day_of_week: Union[int, None] = Query(default=None, description="星期幾"),
    current_time: Union[str, None] = Query(default=None, description="目前時間 (HH:MM) 24H"),
    limit: Union[int, None] = Query(default=1, ge=1, le=10, description="一次回傳的最大的餐廳數量"),
    db: Session = Depends(get_db),
):
    """隨機取得範圍內的餐廳"""

    if day_of_week and current_time:
        random_restaurants = crud.get_restaurant_randomly_with_open_time(
            db, lat, lng, distance, day_of_week, current_time, limit
        )
    else:
        random_restaurants = crud.get_restaurant_randomly(db, lat, lng, distance, limit)

    return restaurant_schema.OnReadsModel(items=random_restaurants)
