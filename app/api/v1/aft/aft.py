from fastapi import APIRouter, FastAPI, Query
from tortoise.expressions import Q

from app.api.v1.utils import insert_log
from app.controllers.aft import aft_controller
from app.models.system import LogType, LogDetailType
from app.schemas.aft import AftSearch
from app.schemas.base import SuccessExtra

router = APIRouter()


@router.post("/list", summary="查看aft列表")
async def _(
        current: int = Query(1, description="页码"),
        size: int = Query(10, description="每页数量"),
        apply_number: str = Query(None, description="申请id"),
        aft_type: str = Query(None, description="aft类型"),
        apply_status: str = Query(None, description="申请状态"),
        remark: str = Query(None, description="备注"),
        nick_name: str = Query(None, description="昵称"),
):
    q = Q()
    if nick_name:
        q &= Q(nick_name__contains=nick_name)
    if apply_number:
        q &= Q(apply_number__contains=apply_number)
    if apply_status:
        q &= Q(apply_status__contains=apply_status)
    if aft_type:
        q &= Q(aft_type=aft_type)
    if remark:
        q &= Q(remark__contains=remark)

    total, aft_objs = await aft_controller.list(page=current, page_size=size, search=q,
                                                order=["id", "-sort"])
    records = []
    for aft_obj in aft_objs:
        record = await aft_obj.to_dict(exclude_fields=["password"])
        await aft_obj.fetch_related("by_account")
        record.update({"nickName": aft_obj.by_account.nickname})
        record.update({"accountNumber": aft_obj.by_account.account_number})
        records.append(record)
    data = {"records": records}
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetList, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)
