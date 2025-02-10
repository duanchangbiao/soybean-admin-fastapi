from typing import Annotated, Optional

from pydantic import BaseModel, Field


class LicenseBase(BaseModel):
    user_name: Annotated[str | None, Field(alias="userName", title="用户名")] = None
    password: Annotated[str | None, Field(title="密码")] = None
    user_email: Annotated[str | None, Field(alias="userEmail", title="邮箱")] = None

    by_user_role_code_list: Annotated[
        list[str] | None, Field(alias="byUserRoleCodeList", title="用户角色编码列表")] = None

    class Config:
        populate_by_name = True


class LicenseCreate(LicenseBase):
    ...


class LicenseUpdate(LicenseBase):
    password: Annotated[str, Field(title="密码")]  # type: ignore
