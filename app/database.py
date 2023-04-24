'''
Author: weijay
Date: 2023-04-24 20:28:52
LastEditors: weijay
LastEditTime: 2023-04-25 00:10:17
Description: Initial DataBase ORM
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

# check_same_thread 只有 SQLite 要設定
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
