from typing import Annotated

from pydantic import BaseModel, Field


class BaseAft(BaseModel):
    apply_number: Annotated[str | None, Field(alias="applyNumber", description="申请id")] = None
    aft_type: Annotated[str | None, Field(alias="aftType", description="aft类型")] = None
    apply_status: Annotated[str | None, Field(alias="applyStatus", description="申请状态")] = None
    remark: Annotated[str | None, Field(alias="remark", description="备注")] = None
    nick_name: Annotated[str | None, Field(alias="nickName", description="昵称")] = None
    TIS_code: Annotated[str | None, Field(alias="tisCode", description="TIS编码")] = None
    standard_name: Annotated[str | None, Field(alias="standardName", description="标准名称")] = None
    update_status: Annotated[str | None, Field(alias="updateStatus", description="更新状态")] = None
    apply_license: Annotated[str | None, Field(alias="applyLicense", description="申请许可证")] = None
    sort: Annotated[str | None, Field(alias="sort", description="排序")] = None
    by_aft_account: Annotated[str | None, Field(alias="accountNumber", title="账号信息")] = None
    create_by: Annotated[str | None, Field(alias="createBy", description="创建人")]
    update_by: Annotated[str | None, Field(aalias="updateBy", description="更新人")]

    class Config:
        populate_by_name = True


class AftSearch(BaseAft):
    current: Annotated[int | None, Field(description="页码")] = None
    size: Annotated[int | None, Field(description="每页数量")] = None


class AftCreate(BaseAft):
    ...


class AftUpdate(BaseAft):
    ...
