'''
Author: weijay
Date: 2023-04-24 22:13:53
LastEditors: weijay
LastEditTime: 2023-05-15 20:53:48
Description: 對資料庫進行 CRUD 操作
'''

from datetime import datetime

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.database import model
from app.schemas import database_schema


# def create_restaurant_open_times(
#     db: Session, restaurant_id: int, open_times: List[restaurant_schema.ResOTCreateModel]
# ):
#     """建立餐廳營業時間

#     為了方便，可以一次新增多個營業時間，但必須是同一個餐廳

#     """

#     db_open_times = []

#     for open_time in open_times:
#         db_open_times.append(
#             model.RestaurantOpenTime(**open_time.dict(), restaurant_id=restaurant_id)
#         )

#     db.add_all(db_open_times)
#     db.commit()


def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    """取得餐廳資料

    Args:
        db (Session): sessionmaker 實例
        skip (int, optional): 要跳過多少筆資料，同等於 `offset`. Defaults to 0.
        limit (int, optional): 最大回傳筆數. Defaults to 100.
    """

    return db.query(model.Restaurant).offset(skip).limit(limit).all()


def create_restaurant(db: Session, restaurant: database_schema.RestaurantDBModel):
    """建立餐廳資料"""

    db_restaurant = model.Restaurant(
        name=restaurant.name,
        address=restaurant.address,
        lat=restaurant.lat,
        lng=restaurant.lng,
        phone=restaurant.phone,
    )

    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


def update_restaurant(
    db: Session, restaurant_id: int, updated_data: database_schema.RestaurantDBModel
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


def get_restaurant_randomly(db: Session, lat: float, lng: float, distance: float, limit: int):
    """隨機取得距離內的餐廳

    Args:
        db (Session): sessionmaker 實例
        lat (float): 所在位置緯度
        lng (float): 所在位置經度
        distance (float): 多少距離範圍內 (km)
        limit (int): 回傳的餐廳數量
    """

    # 這邊使用原生 SQL 指令來查詢
    # 使用 Haversine formula
    sql_text = """
    (
        6371 * 2 * ASIN(
            SQRT(
                POWER(SIN((:lat - ABS(lat)) * PI() / 180 / 2), 2)
                + COS(:lat * PI() / 180)
                * COS(ABS(lat) * PI() / 180)
                * POWER(SIN((:lng - lng) * PI() / 180 / 2), 2)
            )
        )
    ) <= :distance
    """

    items = (
        db.query(model.Restaurant)
        .filter(text(sql_text))
        .params(lat=lat, lng=lng, distance=distance)
        .order_by(func.random())
        .limit(limit)
        .all()
    )

    return items
