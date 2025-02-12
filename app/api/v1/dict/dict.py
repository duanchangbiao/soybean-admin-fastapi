from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.api.v1.utils import insert_log
from app.controllers.dict import dict_controller
from app.models.system import LogType, LogDetailType
from app.schemas.base import SuccessExtra

router = APIRouter()


@router.post("/list", summary="查看dict列表")
async def _(
        current: int = Query(1, description="页码"),
        size: int = Query(10, description="每页数量"),
        dictStatus: str = Query(None, description="字典状态"),
        dictType: str = Query(None, description="字典类型"),
        dictValue: str = Query(None, description="字典键值"),
):
    q = Q()
    if dictStatus:
        q &= Q(dict_status=dictStatus)
    if dictType:
        q &= Q(dict_type=dictType)
    if dictValue:
        q &= Q(dict_value=dictValue)
    total, account_objs = await dict_controller.list(page=current, page_size=size, search=q,
                                                     order=['-ctime'])
    records = []
    for account_obj in account_objs:
        record = await account_obj.to_dict()
        records.append(record)
    data = {"records": records}
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetList, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)
