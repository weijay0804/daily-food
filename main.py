'''
Author: weijay
Date: 2023-04-24 15:56:51
LastEditors: weijay
LastEditTime: 2023-04-25 22:03:36
Description: server 主程式
'''

from app import create_app
from app.routers import register_router

app = create_app("dev")

root_prefix = f"/api/{app.api_version}"

register_router(app, root_prefix)
