'''
Author: weijay
Date: 2023-04-24 23:09:47
LastEditors: weijay
LastEditTime: 2023-05-15 22:06:58
Description: DataBase ORM 模型單元測試
'''

import os
import unittest
from datetime import datetime, time

from sqlalchemy import text

from app.schemas import database_schema
from app.database.model import Restaurant, RestaurantOpenTime
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


class TestRestaurantModel(InitialDataBaseTest):
    """Restaraunt Table ORM 模型單元測試"""

    def setUp(self) -> None:
        # NOTE 如果之後 Restaurant 有做更改的話，這邊要記得改
        fake_restaurant = Restaurant(
            name="測試1",
            address="台北市信義區松壽路6段",
            lat=25.03586,
            lng=121.56433,
            phone="02-1284193212",
        )

        with self.fake_database.get_db() as db:
            db.add(fake_restaurant)
            db.commit()

    def tearDown(self) -> None:
        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant"))
            db.commit()

    def test_create_restaurant(self):
        fake_data = FakeData.fake_restaurant()

        restaurant = Restaurant(**fake_data)

        with self.fake_database.get_db() as db:
            db.add(restaurant)
            db.commit()

            self.assertIsNotNone(restaurant.id)
            self.assertEqual(restaurant.name, fake_data["name"])
            self.assertEqual(restaurant.address, fake_data["address"])
            self.assertEqual(restaurant.lat, fake_data["lat"])
            self.assertEqual(restaurant.lng, fake_data["lng"])
            self.assertEqual(restaurant.phone, None)
            self.assertEqual(restaurant.is_enable, 1)
            self.assertTrue(isinstance(restaurant.create_at, datetime))

    def test_read_restaurant(self):
        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.name == "測試1").first()

        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant.name, "測試1")
        self.assertEqual(restaurant.address, "台北市信義區松壽路6段")
        self.assertEqual(restaurant.lat, 25.03586)
        self.assertEqual(restaurant.lng, 121.56433)
        self.assertEqual(restaurant.phone, "02-1284193212")
        self.assertEqual(restaurant.is_enable, 1)
        self.assertTrue(isinstance(restaurant.create_at, datetime))
        self.assertEqual(restaurant.update_at, None)

    def test_update_restaurant(self):
        fake_data = FakeData.fake_restaurant()

        restaurant = Restaurant(**fake_data)

        with self.fake_database.get_db() as db:
            db.add(restaurant)
            db.commit()

            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

            self.assertEqual(restaurant.address, fake_data["address"])
            self.assertEqual(restaurant.update_at, None)

            restaurant.address = "update_test"
            restaurant.update_at = datetime.utcnow()
            db.commit()

            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

        self.assertEqual(restaurant.address, "update_test")
        self.assertTrue(isinstance(restaurant.update_at, datetime))

    def test_delete_restaurant(self):
        fake_data = FakeData.fake_restaurant()

        restaurant = Restaurant(**fake_data)

        with self.fake_database.get_db() as db:
            db.add(restaurant)
            db.commit()

            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

            self.assertIsNotNone(restaurant)

            db.delete(restaurant)
            db.commit()

            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

        self.assertIsNone(restaurant)


class TestRestaurantOpenTimeModel(InitialDataBaseTest):
    """RestaurantOpenTime ORM 模型單元測試"""

    def setUp(self) -> None:
        # NOTE 如果 restaurant_open_time table 有更改的話，要檢查一下這邊
        fake_restaurant_open_time = RestaurantOpenTime(
            restaurant_id=1,
            day_of_week=1,
            open_time=time(hour=10, minute=0),
            close_time=time(hour=20, minute=0),
        )

        with self.fake_database.get_db() as db:
            db.add(fake_restaurant_open_time)
            db.commit()

    def tearDown(self) -> None:
        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant_open_time"))
            db.commit()

    def test_create_restaurant_open_time(self):
        fake_restaurant_open_time = FakeData.fake_restaurant_open_time()

        with self.fake_database.get_db() as db:
            db.add(RestaurantOpenTime(**fake_restaurant_open_time, restaurant_id=2))
            db.commit()

        with self.fake_database.get_db() as db:
            data = db.query(RestaurantOpenTime).filter(RestaurantOpenTime.id == 2).first()

        self.assertIsNotNone(data)
        self.assertEqual(data.id, 2)
        self.assertEqual(data.day_of_week, fake_restaurant_open_time["day_of_week"])
        self.assertIsInstance(data.open_time, time)
        self.assertEqual(data.open_time, fake_restaurant_open_time["open_time"])
        self.assertIsInstance(data.close_time, time)
        self.assertEqual(data.close_time, fake_restaurant_open_time["close_time"])
        self.assertIsInstance(data.create_at, datetime)
        self.assertIsNotNone(data.create_at)
        self.assertIsNone(data.update_at)

    def test_read_restaurant_open_time(self):
        with self.fake_database.get_db() as db:
            data = (
                db.query(RestaurantOpenTime).filter(RestaurantOpenTime.restaurant_id == 1).first()
            )

        self.assertIsNotNone(data)
        self.assertEqual(data.id, 1)
        self.assertEqual(data.open_time, time(hour=10, minute=0))
        self.assertEqual(data.close_time, time(hour=20, minute=0))

    def test_update_restaurant_open_time(self):
        fake_restaurant_open_time = FakeData.fake_restaurant_open_time()

        with self.fake_database.get_db() as db:
            db.add(RestaurantOpenTime(**fake_restaurant_open_time, restaurant_id=3))
            db.commit()

        with self.fake_database.get_db() as db:
            data = (
                db.query(RestaurantOpenTime).filter(RestaurantOpenTime.restaurant_id == 3).first()
            )

            self.assertIsNone(data.update_at)

            data.open_time = time(hour=12, minute=45)
            data.update_at = datetime.utcnow()

            db.commit()

        with self.fake_database.get_db() as db:
            updated_data = (
                db.query(RestaurantOpenTime).filter(RestaurantOpenTime.restaurant_id == 3).first()
            )

        self.assertEqual(updated_data.day_of_week, fake_restaurant_open_time["day_of_week"])
        self.assertEqual(updated_data.open_time, time(hour=12, minute=45))
        self.assertIsNotNone(updated_data.update_at)

    def test_delete_restaurant_open_time(self):
        fake_restaurant_open_time = FakeData.fake_restaurant_open_time()

        with self.fake_database.get_db() as db:
            db.add(RestaurantOpenTime(**fake_restaurant_open_time, restaurant_id=4))
            db.commit()

        with self.fake_database.get_db() as db:
            data = (
                db.query(RestaurantOpenTime).filter(RestaurantOpenTime.restaurant_id == 4).first()
            )

        self.assertIsNotNone(data)

        with self.fake_database.get_db() as db:
            db.delete(data)
            db.commit()

        with self.fake_database.get_db() as db:
            deleted_data = (
                db.query(RestaurantOpenTime).filter(RestaurantOpenTime.restaurant_id == 4).first()
            )

        self.assertIsNone(deleted_data)
