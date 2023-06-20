'''
Author: weijay
Date: 2023-04-24 15:57:43
LastEditors: andy
LastEditTime: 2023-06-20 02:33:47
Description: 初始化 rotuer
'''

from . import restaurant_router, user_router


def register_router(app, root_prefix):
    """註冊 router"""

    app.include_router(restaurant_router.router, prefix=root_prefix, tags=["餐廳相關路由"])
    app.include_router(user_router.router, prefix=root_prefix, tags=["使用者相關路由"])
