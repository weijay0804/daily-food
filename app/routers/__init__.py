'''
Author: weijay
Date: 2023-04-24 15:57:43
LastEditors: weijay
LastEditTime: 2023-04-25 22:03:27
Description: 初始化 rotuer
'''

from . import restaurant_router


def register_router(app, root_prefix):
    """註冊 router"""

    app.include_router(restaurant_router.router, prefix=root_prefix, tags=["餐廳相關路由"])
