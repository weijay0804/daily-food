'''
Author: andy
Date: 2023-06-20 23:23:55
LastEditors: andy
LastEditTime: 2023-06-21 00:58:56
Description: auth 單元測試
'''

import os
import unittest

from app import auth
from app.database.model import User
from tests.utils import FakeData, FakeDataBase


# TODO 這邊應該獨立出來
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


class TestAuth(InitialDataBaseTest):
    @classmethod
    def setUpClass(cls) -> None:
        """先新增 user 資料"""

        super().setUpClass()

        cls._fake_user = FakeData.fake_user()

        user = User(
            username=cls._fake_user["username"],
            email=cls._fake_user["email"],
            password=cls._fake_user["password_hash"],
        )

        with cls.fake_database.get_db() as db:
            db.add(user)
            db.commit()

    def test_authenticate_user_with_corret_password(self):
        with self.fake_database.get_db() as db:
            user = auth.authenticate_user(
                db, self._fake_user["username"], self._fake_user["password_hash"]
            )

            self.assertTrue(user)

    def test_authenticate_user_with_wrong_password(self):
        with self.fake_database.get_db() as db:
            user = auth.authenticate_user(db, self._fake_user["username"], "wrong password")

            self.assertFalse(user)

    def test_authenticate_user_with_not_exist_user(self):
        with self.fake_database.get_db() as db:
            user = auth.authenticate_user(db, "not exist user", self._fake_user["password_hash"])

            self.assertFalse(user)

    def test_create_access_token(self):
        acess_token = auth.create_access_token({"sub": "test_username"})

        self.assertIsNotNone(acess_token)
