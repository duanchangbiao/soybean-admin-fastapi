from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.api.v1.utils import insert_log
from app.controllers.account import account_controller
from app.models.system import LogType, Dict, LogDetailType
from app.schemas.base import SuccessExtra, Success

router = APIRouter()


@router.post("/list", summary="查看Account列表")
async def _(
        current: int = Query(1, description="页码"),
        size: int = Query(10, description="每页数量"),
        accountNumber: str = Query(None, description="账号信息"),
        nickName: str = Query(None, description="昵称"),
        remark: str = Query(None, description="备注"),
        activated: str = Query(None, description="状态"),
        monitor: str = Query(None, description="监控模块")
):
    q = Q()
    if nickName:
        q &= Q(nick_name__contains=nickName)
    if accountNumber:
        q &= Q(account_number__contains=accountNumber)
    if activated:
        q &= Q(activate__contains=activated)
    if remark:
        q &= Q(remark__contains=remark)
    if monitor:
        if _by_dict := await Dict.get_or_none(dict_value=monitor) is not None:
            q &= Q(by_account_dict=_by_dict)
        else:
            return Success(msg="字典信息不正确", code=2000)
    total, account_objs = await account_controller.list(page=current, page_size=size, search=q,
                                                        order=["id", "-sort"])
    records = []
    for account_obj in account_objs:
        record = await account_obj.to_dict(exclude_fields=["by_account_dict"])
        await account_obj.fetch_related("by_account_dict")
        account_monitor_list = [by_account_dict.to_dict() for by_account_dict in account_obj.by_account_dict]
        record.update({"accountMonitorList": account_monitor_list})
        records.append(record)
    data = {"records": records}
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetList, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)
