from pydantic import BaseModel, Field
from typing import Annotated


class BaseMor(BaseModel):
    apply_number: Annotated[str | None, Field(alias="applyNumber", description="申请id")] = None
    TIS_code: Annotated[str | None, Field(alias="tisCode", description="TIS编码")] = None
    standard_name: Annotated[str | None, Field(alias="standardName", description="标准名称")] = None
    apply_license: Annotated[str | None, Field(alias="applyLicense", description="申请许可证")] = None
    apply_date: Annotated[str | None, Field(alias="applyDate", description="申请日期")] = None
    update_status: Annotated[str | None, Field(alias="updateStatus", description="更新状态")] = None
    apply_tax: Annotated[str | None, Field(alias="applyTax", description="申请税号")] = None
    apply_status: Annotated[str | None, Field(alias="applyStatus", description="申请状态")] = None
    mor_type: Annotated[str | None, Field(alias="morType", description="aft类型")] = None
    sort: Annotated[str | None, Field(alias="sort", description="排序")] = None
    remark: Annotated[str | None, Field(alias="remark", description="备注")] = None
    nick_name: Annotated[str | None, Field(alias="nickName", description="昵称")] = None
    by_mor_account: Annotated[str | None, Field(alias="accountNumber", title="账号信息")] = None

    class Config:
        populate_by_name = True


class MorCreate(BaseMor):
    ...


class MorUpdate(BaseMor):
    ...


class MorSearch(BaseMor):
    current: Annotated[int | None, Field(description="页码")] = None
    size: Annotated[int | None, Field(description="每页数量")] = None
