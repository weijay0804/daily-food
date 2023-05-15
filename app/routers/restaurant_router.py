'''
Author: weijay
Date: 2023-04-24 15:58:18
LastEditors: weijay
LastEditTime: 2023-05-15 20:53:36
Description: 餐廳路由
'''

from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas import restaurant_schema, database_schema
from app.database import SessionLocal
from app.database import crud
from app.utils import MapApi

router = APIRouter(prefix="/restaurant")


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/", response_model=restaurant_schema.ReadsModel)
def read_restaurants(db: Session = Depends(get_db)):
    """取得所有餐廳"""

    items = crud.get_restaurants(db)

    return restaurant_schema.ReadsModel(items=items)


# 這裡改成分開傳送資料比較好 open_time
@router.post("/", status_code=201)
def create_restaurant(items: restaurant_schema.CreateOrUpdateModel, db: Session = Depends(get_db)):
    """新增餐廳"""

    # 使用第三方 Api 取得經緯度
    lat, lng = MapApi().get_coords(items.address)

    full_item = database_schema.RestaurantDBModel(**items.dict(), lat=lat, lng=lng)

    if not (lat and lng):
        raise HTTPException(
            status_code=400,
            detail=f"The address '{items.address}' format is incorrect and cannot be processed correctly",
        )

    crud.create_restaurant(db, full_item)

    return {"message": "created."}


@router.patch("/{restaurant_id}", response_model=restaurant_schema.ReadModel)
def update_restaurant(
    restaurant_id: str, item: restaurant_schema.CreateOrUpdateModel, db: Session = Depends(get_db)
):
    """更新餐廳"""

    updated_restaurant = crud.update_restaurant(db, restaurant_id, item)

    if not updated_restaurant:
        raise HTTPException(
            status_code=404,
            detail=f"The restaurant ID: {restaurant_id} is not founded in database.",
        )

    return updated_restaurant


@router.delete("/{restaurant_id}", status_code=200)
def delete_restaurant(restaurant_id: str, db: Session = Depends(get_db)):
    """刪除餐廳"""

    deleted_restaurant = crud.delete_restaurant(db, restaurant_id)

    if not deleted_restaurant:
        raise HTTPException(
            status_code=404,
            detail=f"The restaurant ID: {restaurant_id} is not founded in database.",
        )

    return {"message": f"Restaurant ID {deleted_restaurant.id} has been deleted."}


@router.get("/choice", response_model=restaurant_schema.ReadsModel)
def read_restaurant_randomly(
    lat: float = Query(default=..., description="所在位置的緯度值"),
    lng: float = Query(default=..., description="所在位置的經度值"),
    distance: float = Query(default=..., description="要查詢多少距離範圍內 (km)"),
    limit: Union[int, None] = Query(default=1, ge=1, le=10, description="一次回傳的最大的餐廳數量"),
    db: Session = Depends(get_db),
):
    """隨機取得範圍內的餐廳ㄧ"""

    random_restaurants = crud.get_restaurant_randomly(db, lat, lng, distance, limit)

    return restaurant_schema.ReadsModel(items=random_restaurants)
