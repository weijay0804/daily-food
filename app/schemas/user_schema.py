'''
Author: andy
Date: 2023-06-20 02:27:31
LastEditors: andy
LastEditTime: 2023-06-20 22:53:57
Description: 定義 user router 的數據模型
'''

from pydantic import BaseModel


class OnReadNoOAuthModel(BaseModel):
    id: int
    username: str
    email: str


class OnCreateNoOAuthModel(BaseModel):
    """建立不是用 OAuth 的使用者 schema"""

    username: str
    email: str
    password: str
