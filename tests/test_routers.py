'''
Author: weijay
Date: 2023-04-25 16:26:37
LastEditors: weijay
LastEditTime: 2023-07-10 22:04:03
Description: Api Router 單元測試
'''


import unittest
from unittest import mock

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.config import config
from app import create_app
from app.database.model import Restaurant, RestaurantOpenTime, User
from app.routers import register_router
from tests.utils import FakeDataBase, FakeData
from app.routers.depends import get_db


ROOT_URL = "/api/v1"


class InitialTestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_app = create_app("test")

        register_router(cls.test_app, f"/api/{config.TestConfig.API_VERSION}")

        cls.fake_database = FakeDataBase()

        cls.fake_database.Base.metadata.create_all(bind=cls.fake_database.engine)

        cls.client = TestClient(cls.test_app)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.fake_database.engine.clear_compiled_cache()
        cls.fake_database.engine.dispose()
        cls.fake_database.Base.metadata.drop_all(bind=cls.fake_database.engine)


class TestResaurantRotuer(InitialTestClient):
    def setUp(self) -> None:
        self.test_app.dependency_overrides[get_db] = self.fake_database.override_get_db

    def tearDown(self) -> None:
        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant"))
            db.commit()

    def test_read_restaurant_router(self):
        fake_data = FakeData.fake_restaurant()
        restaurant = Restaurant(**fake_data)

        with self.fake_database.get_db() as db:
            db.add(restaurant)
            db.commit()

        response = self.client.get(f"{ROOT_URL}/restaurant")

        data = response.json()["items"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        self.assertIsNotNone(data[0]["name"])
        self.assertIsNotNone(data[0]["address"])

    # 使用 測試方法層面 mock 直接替換掉 get_coords()
    @mock.patch("app.utils.MapApi.get_coords", return_value=(25.0, 121.0))
    def test_create_restaurant_router(self, mock_get_coords):
        fake_restaurant = FakeData.fake_restaurant(is_lat_lng=False)
        response = self.client.post(
            f"{ROOT_URL}/restaurant",
            json=fake_restaurant,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "created."})

    def test_upate_restaurant_router(self):
        fake_data = FakeData.fake_restaurant()
        with self.fake_database.get_db() as db:
            db.add(Restaurant(**fake_data))
            db.commit()

        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

        response = self.client.patch(
            f"{ROOT_URL}/restaurant/{restaurant.id}",
            json={
                "name": "測試餐廳更新",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_restaurant_router(self):
        fake_data = FakeData.fake_restaurant()

        with self.fake_database.get_db() as db:
            db.add(Restaurant(**fake_data))
            db.commit()

        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

        response = self.client.delete(f"{ROOT_URL}/restaurant/{restaurant.id}")

        self.assertEqual(response.status_code, 200)


class TestChoiceRestaurantRouter(InitialTestClient):
    """隨機選擇餐廳路由測試"""

    def setUp(self) -> None:
        self.test_app.dependency_overrides[get_db] = self.fake_database.override_get_db

    def tearDown(self) -> None:
        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant"))
            db.commit()

    def test_read_retaurant_randomly_router(self):
        inner_fake_data1, inner_fake_data2 = FakeData.fake_restaurant(number=2)
        outer_fake_data = FakeData.fake_restaurant_far()

        with self.fake_database.get_db() as db:
            db.add_all(
                [
                    Restaurant(**inner_fake_data1),
                    Restaurant(**inner_fake_data2),
                    Restaurant(**outer_fake_data),
                ]
            )

            db.commit()

        lat, lng = FakeData.fake_current_location()
        distance = 5.0

        response = self.client.get(
            f"{ROOT_URL}/restaurant/choice?lat={lat}&lng={lng}&distance={distance}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.json()['items'][0]["name"]
            in (inner_fake_data1["name"], inner_fake_data2["name"])
        )
        self.assertEqual(len(response.json()['items']), 1)

        response = self.client.get(
            f"{ROOT_URL}/restaurant/choice?lat={lat}&lng={lng}&distance={distance}&limit=2"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['items']), 2)

    def test_read_retaurant_randomly_router_with_open_time(self):
        fake_data1, fake_data2 = FakeData.fake_restaurant(number=2)

        fake_open_time1, fake_open_time2 = FakeData.fake_restaurant_open_time(number=2)

        restaurant1 = Restaurant(**fake_data1)
        restaurant2 = Restaurant(**fake_data2)

        with self.fake_database.get_db() as db:
            db.add_all([restaurant1, restaurant2])
            db.commit()
            db.refresh(restaurant1)
            db.refresh(restaurant2)

            open_time1 = RestaurantOpenTime(**fake_open_time1)
            open_time2 = RestaurantOpenTime(**fake_open_time2)

            restaurant1.open_times.append(open_time1)
            restaurant2.open_times.append(open_time2)

            db.add_all([open_time1, open_time2])
            db.commit()

            db.refresh(open_time1)
            db.refresh(open_time2)

        lat, lng = FakeData.fake_current_location()
        distance = 5.0
        day_of_week = open_time1.day_of_week
        current_time = open_time1.open_time.strftime("%H:%M")

        response = self.client.get(
            f"{ROOT_URL}/restaurant/choice?lat={lat}&lng={lng}&distance={distance}&day_of_week={day_of_week}&current_time={current_time}&limit=2"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 1)


class TestRestaurantOpenTimeRouter(InitialTestClient):
    def to_datetime(self, str):
        import datetime

        return datetime.datetime.strptime(str, "%H:%M:%S").time()

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        fake_reatuant = FakeData.fake_restaurant()

        db_restaurant = Restaurant(**fake_reatuant)

        with cls.fake_database.get_db() as db:
            db.add(db_restaurant)
            db.commit()
            db.refresh(db_restaurant)

        cls.fake_restaurant_id = db_restaurant.id

    def setUp(self) -> None:
        self.test_app.dependency_overrides[get_db] = self.fake_database.override_get_db

    def tearDown(self) -> None:
        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant_open_time"))
            db.commit()

    def test_create_restaurant_open_time_router(self):
        items = FakeData.fake_restaurant_open_time(to_str=True, number=2)
        response = self.client.post(
            f"{ROOT_URL}/restaurant/{self.fake_restaurant_id}/open_time", json={"items": items}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "created."})

    def test_upadte_restaurant_open_time_router(self):
        fake_open_time = FakeData.fake_restaurant_open_time()

        db_open_time = RestaurantOpenTime(**fake_open_time)

        with self.fake_database.get_db() as db:
            r_obj = db.get(Restaurant, self.fake_restaurant_id)

            r_obj.open_times.append(db_open_time)

            db.add(db_open_time)
            db.commit()
            db.refresh(db_open_time)

        response = self.client.patch(
            f"{ROOT_URL}/restaurant/open_time/{db_open_time.id}",
            json={"day_of_week": 100},
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_restaurant_open_time_router(self):
        fake_open_time = FakeData.fake_restaurant_open_time()

        db_open_time = RestaurantOpenTime(**fake_open_time)

        with self.fake_database.get_db() as db:
            r_obj = db.get(Restaurant, self.fake_restaurant_id)
            r_obj.open_times.append(db_open_time)
            db.add(db_open_time)
            db.commit()
            db.refresh(db_open_time)

        response = self.client.delete(f"{ROOT_URL}/restaurant/open_time/{db_open_time.id}")

        self.assertEqual(response.status_code, 200)


class TestUserRouter(InitialTestClient):
    def setUp(self) -> None:
        self.test_app.dependency_overrides[get_db] = self.fake_database.override_get_db

    def tearDown(self) -> None:
        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM user"))
            db.commit()

    def test_user_register(self):
        fake_data = FakeData.fake_user()

        response = self.client.post(
            f"{ROOT_URL}/user/",
            json={
                "username": fake_data["username"],
                "email": fake_data["email"],
                "password": fake_data["password"],
            },
        )

        self.assertEqual(response.status_code, 201)

    def test_user_register_with_exist_username(self):
        fake_data = FakeData.fake_user()

        with self.fake_database.get_db() as db:
            db.add(User(**fake_data))
            db.commit()

        response = self.client.post(
            f"{ROOT_URL}/user",
            json={
                "username": fake_data["username"],
                "email": fake_data["email"] + "test",
                "password": fake_data["password"],
            },
        )

        self.assertEqual(response.status_code, 409)

    def test_user_register_with_exist_email(self):
        fake_data = FakeData.fake_user()

        with self.fake_database.get_db() as db:
            db.add(User(**fake_data))
            db.commit()

        response = self.client.post(
            f"{ROOT_URL}/user",
            json={
                "username": fake_data["username"] + "test",
                "email": fake_data["email"],
                "password": fake_data["password"],
            },
        )

        self.assertEqual(response.status_code, 409)

    def test_user_login(self):
        fake_user = FakeData.fake_user()
        db_user = User(
            username=fake_user["username"],
            email=fake_user["email"],
            password=fake_user["password"],
        )

        with self.fake_database.get_db() as db:
            db.add(db_user)
            db.commit()

        response = self.client.post(
            f"{ROOT_URL}/user/token",
            data={"username": fake_user["username"], "password": fake_user["password"]},
            headers={"WWW-Authenticate": "Bearer"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json().get("access_token"))
        self.assertEqual(response.json().get("token_type"), "bearer")

    def test_user_login_with_invalid_username(self):
        fake_user = FakeData.fake_user()

        with self.fake_database.get_db() as db:
            db.add(User(**fake_user))
            db.commit()

        response = self.client.post(
            f"{ROOT_URL}/user/token",
            data={"username": fake_user["username"] + "test", "password": fake_user["password"]},
            headers={"WWW-Authenticate": "Bearer"},
        )

        self.assertEqual(response.status_code, 401)

    def test_user_login_with_invalid_password(self):
        fake_user = FakeData.fake_user()

        with self.fake_database.get_db() as db:
            db.add(User(**fake_user))
            db.commit()

        response = self.client.post(
            f"{ROOT_URL}/user/token",
            data={"username": fake_user["username"], "password": fake_user["password"] + "test"},
            headers={"WWW-Authenticate": "Bearer"},
        )

        self.assertEqual(response.status_code, 401)
