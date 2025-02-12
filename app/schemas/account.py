from typing import Annotated

from pydantic import Field

from app.models.system import BaseModel


class BaseAccount(BaseModel):
    account_number: Annotated[str | None, Field(alias="accountNumber", title="账号信息")] = None
    nick_name: Annotated[str | None, Field(alias="nickName", description="昵称")] = None
    remark: Annotated[str | None, Field(alias="remark", description="备注")] = None
    activated: Annotated[str | None, Field(alias="activated", description="状态")] = None
    by_account_modules: Annotated[str | None, Field(alias="monitor", description="模块")] = None

    class Config:
        populate_by_name = True


class AccountCreate(BaseAccount):
    ...


class AccountUpdate(BaseAccount):
    ...


class AccountSearch(BaseAccount):
    current: Annotated[int | None, Field(description="页码")] = None
    size: Annotated[int | None, Field(description="每页数量")] = None
