'''
Author: andy
Date: 2023-06-20 22:52:50
LastEditors: andy
LastEditTime: 2023-06-20 22:53:00
Description: 定義跟使用者認證相關的 schema
'''

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """JWT Token schema"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT Token data schema"""

    username: Optional[str] = None
