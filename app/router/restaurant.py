'''
Author: weijay
Date: 2023-04-24 15:58:18
LastEditors: weijay
LastEditTime: 2023-04-24 19:26:18
Description: 餐廳路由
'''

from fastapi import APIRouter

from app.schemas.restaurant_schemes import ResReadModel, ResCreateModel

router = APIRouter(prefix="/restaurant")


@router.get("/", response_model=ResReadModel)
def read_restaurant():
    pass


@router.post("/", status_code=201)
def create_restaurant(item: ResCreateModel):
    pass


@router.patch("/{restaurant_id}", response_model=ResCreateModel)
def update_restaurant(restaurant_id: str, item: ResCreateModel):
    pass


@router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant(restaurant_id: str):
    pass
