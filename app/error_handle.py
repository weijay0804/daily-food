'''
Author: weijay
Date: 2023-05-22 19:21:36
LastEditors: andy
LastEditTime: 2023-06-20 22:50:25
Description: 定義常見的錯誤
'''

from typing import Union

from fastapi import HTTPException, status


__all__ = ["ErrorHandler"]


class ErrorDesc:
    """定義默認的錯誤訊息"""

    ERROR_400 = "Bad request."
    ERROR_404 = "The item you requested does not exist."


class CustomError:
    """自訂錯誤"""

    def credentials_execption():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class ErrorHandler:
    """錯誤處理"""

    def raise_400(desc: Union[str, None] = None):
        """raise 400 error"""

        if desc:
            error_desc = desc

        else:
            error_desc = ErrorDesc.ERROR_400

        raise HTTPException(status_code=400, detail=error_desc)

    def raise_404(desc: Union[str, None] = None):
        """raise 404 error"""

        if desc:
            error_desc = desc

        else:
            error_desc = ErrorDesc.ERROR_404

        raise HTTPException(status_code=404, detail=error_desc)
