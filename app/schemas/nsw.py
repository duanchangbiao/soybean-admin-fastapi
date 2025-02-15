from app.models.system import BaseModel
from pydantic import BaseModel, Field
from typing import Annotated


class BaseNsw(BaseModel):
    apply_number: Annotated[str | None, Field(alias="applyNumber", description="申请id")] = None
    invoice: Annotated[str | None, Field(alias="invoice", description="发票")] = None
    invoice_date: Annotated[str | None, Field(alias="invoiceDate", description="发票单号")] = None
    product_number: Annotated[str | None, Field(alias="productNumber", description="产品数量")] = None
    update_status: Annotated[str | None, Field(alias="updateStatus", description="更新状态")] = None
    rpg_group: Annotated[str | None, Field(alias="rpgGroup", description="责任小组")] = None
    apply_date: Annotated[str | None, Field(alias="applyDate", description="申请日期")] = None
    apply_status: Annotated[str | None, Field(alias="applyStatus", description="申请状态")] = None
    pass_date: Annotated[str | None, Field(alias="passDate", description="aft类型")] = None
    sort: Annotated[str | None, Field(alias="sort", description="排序")] = None
    remark: Annotated[str | None, Field(alias="remark", description="备注")] = None
    nick_name: Annotated[str | None, Field(alias="nickName", description="昵称")] = None
    by_nsw_account: Annotated[str | None, Field(alias="accountNumber", title="账号信息")] = None
    create_by: Annotated[str | None, Field(alias="createBy", description="创建人")] = None
    update_by: Annotated[str | None, Field(aalias="updateBy", description="更新人")] = None

    class Config:
        populate_by_name = True


class NswCreate(BaseNsw):
    ...


class NswUpdate(BaseNsw):
    ...


class NswSearch(BaseNsw):
    current: Annotated[int | None, Field(description="页码")] = None
    size: Annotated[int | None, Field(description="每页数量")] = None
