'''
Author: weijay
Date: 2023-04-24 15:56:51
LastEditors: weijay
LastEditTime: 2023-04-24 17:55:41
Description: server 主程式
'''

from app import create_app
from app.router import restaurant

app = create_app("dev")

root_prefix = f"/api/{app.api_version}"
