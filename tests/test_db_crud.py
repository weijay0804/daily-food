'''
Author: weijay
Date: 2023-05-15 22:05:37
LastEditors: weijay
LastEditTime: 2023-05-15 22:05:58
Description: DataBase CRUD 單元測試
'''

import os
import unittest

from sqlalchemy import text

from app.schemas import database_schema
from app.database.model import Restaurant
from app.database import crud
from tests.utils import FakeData, FakeDataBase


class InitialDataBaseTest(unittest.TestCase):
    """建立測試資料庫環境"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.fake_database = FakeDataBase()
        cls.fake_database.Base.metadata.create_all(bind=cls.fake_database.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.fake_database.engine.clear_compiled_cache()
        cls.fake_database.engine.dispose()
        cls.fake_database.Base.metadata.drop_all(bind=cls.fake_database.engine)
        os.remove("test.db")


class TestRestaurantCURD(InitialDataBaseTest):
    def tearDown(self) -> None:
        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant"))
            db.commit()

    def test_get_restaurants_function(self):
        fake_data = []

        for _ in range(2):
            data = FakeData.fake_restaurant()
            fake_data.append(Restaurant(**data))

        with self.fake_database.get_db() as db:
            db.add_all(fake_data)
            db.commit()
            db.close()

        with self.fake_database.get_db() as db:
            restaurants = crud.get_restaurants(db)

        self.assertTrue(isinstance(restaurants, list))
        self.assertTrue(isinstance(restaurants[0], Restaurant))

    def test_create_restaurant_function(self):
        fake_data = FakeData.fake_restaurant()

        restaurant = database_schema.RestaurantDBModel(**fake_data, phone="0932212849")

        with self.fake_database.get_db() as db:
            db_restaurant = crud.create_restaurant(db, restaurant)

        self.assertIsNotNone(db_restaurant)
        self.assertTrue(isinstance(db_restaurant, Restaurant))
        self.assertEqual(db_restaurant.name, fake_data["name"])

    def test_update_restaurant_function(self):
        fake_data = FakeData.fake_restaurant()

        with self.fake_database.get_db() as db:
            db.add(Restaurant(**fake_data))
            db.commit()

        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

            update_data = database_schema.RestaurantDBModel(
                name="測試2更新", address=restaurant.address, lat=restaurant.lat, lng=restaurant.lng
            )

            updated_restaurant = crud.update_restaurant(db, restaurant.id, update_data)

        self.assertIsNotNone(updated_restaurant)
        self.assertEqual(updated_restaurant.name, "測試2更新")
        self.assertEqual(updated_restaurant.address, restaurant.address)
        self.assertEqual(updated_restaurant.phone, restaurant.phone)

    def test_update_restaurant_function_with_not_exist_id(self):
        fake_data = FakeData.fake_restaurant()

        update_data = database_schema.RestaurantDBModel(**fake_data)

        with self.fake_database.get_db() as db:
            upadted_restaurant = crud.update_restaurant(db, 1000, update_data)

        self.assertIsNone(upadted_restaurant)

    def test_delete_restaurant_function(self):
        fake_data = FakeData.fake_restaurant()

        with self.fake_database.get_db() as db:
            db.add(Restaurant(**fake_data))
            db.commit()

        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

            crud.delete_restaurant(db, restaurant.id)

            deleted_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant.id).first()

        self.assertIsNotNone(restaurant)
        self.assertIsNone(deleted_restaurant)

    def test_delete_restaurant_function_with_not_eixst_id(self):
        with self.fake_database.get_db() as db:
            deleted_restaurant = crud.delete_restaurant(db, 1000)

        self.assertIsNone(deleted_restaurant)

    def test_get_restaurant_randomly_function(self):
        fake_inner_data = FakeData.fake_restaurant()
        fake_outer_data = FakeData.fake_restaurant_far()

        inner_restaurant = Restaurant(**fake_inner_data)
        outer_restaurant = Restaurant(**fake_outer_data)

        with self.fake_database.get_db() as db:
            db.add_all([inner_restaurant, outer_restaurant])
            db.commit()

            inner_lat, inner_lng = FakeData.fake_current_location()
            random_restaurant = crud.get_restaurant_randomly(db, inner_lat, inner_lng, 5.0, 1)

        self.assertIsNotNone(random_restaurant)
        self.assertEqual(random_restaurant[0].name, fake_inner_data["name"])
        self.assertEqual(len(random_restaurant), 1)
