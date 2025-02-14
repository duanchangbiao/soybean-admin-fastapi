from typing import Annotated

from pydantic import BaseModel, Field


class BaseAccount(BaseModel):
    account_number: Annotated[str | None, Field(alias="accountNumber", title="账号信息")] = None
    nickname: Annotated[str | None, Field(alias="nickname", description="昵称")] = None
    remark: Annotated[str | None, Field(alias="remark", description="备注")] = None
    activate: Annotated[str | None, Field(alias="activate", description="状态")] = None
    feedback: Annotated[str | None, Field(alias="feedback", description="反馈")] = None
    password: Annotated[str | None, Field(alias="password", description="密码")] = None
    by_account_modules: Annotated[list[int] | None, Field(alias="accountMonitorList", title="account编码列表")] = None
    create_by: Annotated[str | None, Field(alias="createBy", description="创建人")] = None
    update_by: Annotated[str | None, Field(alias="updateBy", description="更新人")] = None

    class Config:
        populate_by_name = True


class AccountCreate(BaseAccount):
    ...


class AccountUpdate(BaseAccount):
    ...


class AccountSearch(BaseAccount):
    current: Annotated[int | None, Field(description="页码")] = None
    size: Annotated[int | None, Field(description="每页数量")] = None
