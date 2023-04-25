'''
Author: weijay
Date: 2023-04-24 15:58:18
LastEditors: weijay
LastEditTime: 2023-04-25 16:07:11
Description: 餐廳路由
'''

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.restaurant_scheme import ResReadModel, ResCreateModel, ResModel
from app.database import SessionLocal
from app import crud

router = APIRouter(prefix="/restaurant")

fake_data: List[ResReadModel] = []


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/", response_model=ResReadModel)
def read_restaurant(db: Session = Depends(get_db)):
    items = crud.get_restaurants(db)

    return ResReadModel(items=items)


@router.post("/", status_code=201)
def create_restaurant(items: ResCreateModel, db: Session = Depends(get_db)):
    crud.create_restaurant(db, items)

    return {"message": "created."}


@router.patch("/{restaurant_id}", response_model=ResModel)
def update_restaurant(restaurant_id: str, item: ResCreateModel, db: Session = Depends(get_db)):
    updated_restaurant = crud.update_restaurant(db, restaurant_id, item)

    if not updated_restaurant:
        raise HTTPException(
            status_code=404,
            detail=f"The restaurant ID: {restaurant_id} is not founded in database.",
        )

    return updated_restaurant


@router.delete("/{restaurant_id}", status_code=200)
def delete_restaurant(restaurant_id: str, db: Session = Depends(get_db)):
    deleted_restaurant = crud.delete_restaurant(db, restaurant_id)

    if not deleted_restaurant:
        raise HTTPException(
            status_code=404,
            detail=f"The restaurant ID: {restaurant_id} is not founded in database.",
        )

    return {"message": f"Restaurant ID {deleted_restaurant.id} has been deleted."}
