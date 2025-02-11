from fastapi import APIRouter, FastAPI, Query
from tortoise.expressions import Q

from app.api.v1.utils import insert_log
from app.controllers.aft import aft_controller
from app.models.system import LogType, LogDetailType, Account
from app.schemas.aft import AftSearch
from app.schemas.base import SuccessExtra, Success

router = APIRouter()


@router.post("/list", summary="查看aft列表")
async def _(
        current: int = Query(1, description="页码"),
        size: int = Query(10, description="每页数量"),
        applyNumber: str = Query(None, description="申请id"),
        aftType: str = Query(None, description="aft类型"),
        applyStatus: str = Query(None, description="申请状态"),
        remark: str = Query(None, description="备注"),
        nickName: str = Query(None, description="昵称"),
):
    q = Q()
    if nickName:
        if _by_account := await Account.get_or_none(nickname=nickName) is not None:
            q &= Q(by_account=_by_account)
        else:
            return Success(msg="账号不存在", code=2000)
    if applyNumber:
        q &= Q(apply_number__contains=applyNumber)
    if applyStatus:
        q &= Q(apply_status__contains=applyStatus)
    if aftType:
        q &= Q(aft_type=aftType)
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
