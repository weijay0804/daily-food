'''
Author: weijay
Date: 2023-04-25 17:19:24
LastEditors: weijay
LastEditTime: 2023-04-27 16:06:36
Description: 放一些測試時會用到的通用函示
'''

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.model import Base


class FakeDataBase:
    """產生測試資料庫"""

    SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

    def __init__(self):
        self.engine = create_engine(
            self.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )

        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        self.Base = Base

    def override_get_db(self):
        try:
            db = self.SessionLocal()
            yield db

        finally:
            db.close()

    @contextmanager
    def get_db(self):
        try:
            db = self.SessionLocal()
            yield db

        finally:
            db.close()
