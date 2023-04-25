'''
Author: weijay
Date: 2023-04-24 22:13:53
LastEditors: weijay
LastEditTime: 2023-04-26 01:23:56
Description: 對資料庫進行 CRUD 操作
'''

from datetime import datetime

from sqlalchemy.orm import Session

from app.database import model
from app.schemas import restaurant_scheme


def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    """取得餐廳資料

    Args:
        db (Session): sessionmaker 實例
        skip (int, optional): 要跳過多少筆資料，同等於 `offset`. Defaults to 0.
        limit (int, optional): 最大回傳筆數. Defaults to 100.
    """

    return db.query(model.Restaurant).offset(skip).limit(limit).all()


def create_restaurant(db: Session, restaurant: restaurant_scheme.ResCreateModel):
    """建立餐廳資料"""

    db_restaurant = model.Restaurant(
        name=restaurant.name,
        address=restaurant.address,
        lat=23.0001,
        lng=120.222,
        phone=restaurant.phone,
    )

    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


def update_restaurant(
    db: Session, restaurant_id: int, updated_data: restaurant_scheme.ResCreateModel
):
    """更新餐廳資料，如果資料庫中找不到傳進來的 `restaurant_id` 資料，則回傳 `None`"""

    restaurant = db.query(model.Restaurant).filter(model.Restaurant.id == restaurant_id).first()

    if not restaurant:
        return None

    # 只要更新有傳入的資料就好，其他欄位如果沒有更新，就照舊
    for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(restaurant, field, value)

    restaurant.update_at = datetime.utcnow()

    db.commit()
    db.refresh(restaurant)

    return restaurant


def delete_restaurant(db: Session, restaurant_id: int):
    """刪除餐廳資料，如果資料庫中找不到傳進來的 `restaurant_id` 資料，則回傳 `None`"""

    restaurant = db.query(model.Restaurant).filter(model.Restaurant.id == restaurant_id).first()

    if not restaurant:
        return None

    db.delete(restaurant)
    db.commit()

    return restaurant
