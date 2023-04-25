'''
Author: weijay
Date: 2023-04-24 20:28:52
LastEditors: weijay
LastEditTime: 2023-04-26 01:17:05
Description: Initial DataBase ORM
'''

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("DATABASE_URL"):
    SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

# check_same_thread 只有 SQLite 要設定
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_args = {"connect_args": {"check_same_thread": False}}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
