'''
Author: weijay
Date: 2023-04-24 15:58:18
LastEditors: weijay
LastEditTime: 2023-04-26 01:23:52
Description: 餐廳路由
'''

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.restaurant_scheme import ResReadModel, ResCreateModel, ResModel
from app.database import SessionLocal
from app.database import crud

router = APIRouter(prefix="/restaurant")


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/", response_model=ResReadModel)
def read_restaurants(db: Session = Depends(get_db)):
    """取得所有餐廳"""

    items = crud.get_restaurants(db)

    return ResReadModel(items=items)


@router.post("/", status_code=201)
def create_restaurant(items: ResCreateModel, db: Session = Depends(get_db)):
    """新增餐廳"""

    crud.create_restaurant(db, items)

    return {"message": "created."}


@router.patch("/{restaurant_id}", response_model=ResModel)
def update_restaurant(restaurant_id: str, item: ResCreateModel, db: Session = Depends(get_db)):
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
