from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.api.v1.utils import insert_log
from app.controllers.mor import mor_controller
from app.models.system import Account, LogType, LogDetailType
from app.schemas.base import Success, SuccessExtra
from app.schemas.mor import MorCreate, MorUpdate

router = APIRouter()


@router.post("/list", summary="查看Mor列表")
async def _(
        current: int = Query(1, description="页码"),
        size: int = Query(10, description="每页数量"),
        applyNumber: str = Query(None, description="申请id"),
        morType: str = Query(None, description="aft类型"),
        applyStatus: str = Query(None, description="申请状态"),
        remark: str = Query(None, description="备注"),
        nickName: str = Query(None, description="昵称"),
):
    q = Q()
    if nickName:
        if _by_account := await Account.get_or_none(nickname=nickName) is not None:
            q &= Q(by_mor_account=_by_account)
        else:
            return Success(msg="账号不存在", code=2000)
    if applyNumber:
        q &= Q(apply_number__contains=applyNumber)
    if applyStatus:
        q &= Q(apply_status__contains=applyStatus)
    if morType:
        q &= Q(mor_type=morType)
    if remark:
        q &= Q(remark__contains=remark)

    total, aft_objs = await mor_controller.list(page=current, page_size=size, search=q,
                                                order=["id", "-sort"])
    records = []
    for aft_obj in aft_objs:
        record = await aft_obj.to_dict(exclude_fields=["by_mor_account"])
        await aft_obj.fetch_related("by_mor_account")
        account = await aft_obj.by_mor_account
        if len(account) != 0:
            record.update({"nickName": account[0].nickname})
            record.update({"accountNumber": account[0].account_number})
        records.append(record)
    data = {"records": records}
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetList, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.get("/get/{mor_id}", summary="查看Mor")
async def get_user(mor_id: int):
    user_obj = await mor_controller.get(id=mor_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetOne, by_user_id=0)
    return Success(data=await user_obj.to_dict(exclude_fields=["by_mor_account"]))


@router.post("/add", summary="创建Mor")
async def _(mor_in: MorCreate):
    if not mor_in.by_mor_account:
        return Success(code="4090", msg="The aft must have account number that exists.")
    account = await mor_controller.get_by_account_number(account_number=mor_in.by_mor_account)
    if not account:
        return Success(code="4090", msg="The account number is not exists.")
    new_aft = await mor_controller.create(obj_in=mor_in, exclude={"by_mor_account"})
    await mor_controller.update_mor_account(new_aft, mor_in.by_mor_account)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserCreateOne, by_user_id=0)
    return Success(msg="Created Successfully", data={"created_id": new_aft.id})


@router.patch("/update/{mor_id}", summary="更新mor")
async def _(mor_id: int, mor_in: MorUpdate):
    if not mor_in.by_mor_account:
        return Success(code="4090", msg="The aft must have account number that exists.")
    account = await mor_controller.get_by_account_number(account_number=mor_in.by_mor_account)
    if not account:
        return Success(code="4090", msg="The account number is not exists.")
    mor = await mor_controller.update(id=mor_id, obj_in=mor_in, exclude={"by_mor_account"})
    await mor_controller.update_mor_account(mor, mor_in.by_mor_account)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserUpdateOne, by_user_id=0)
    return Success(msg="Updated Successfully", data={"updated_id": mor_id})


@router.delete("/delete/{mor_id}", summary="删除mor")
async def _(mor_id: int):
    await mor_controller.remove(id=mor_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserDeleteOne, by_user_id=0)
    return Success(msg="Deleted Successfully", data={"deleted_id": mor_id})


@router.delete("/batch", summary="批量删除mor")
async def _(ids: str = Query(..., description="删除aft列表, 用逗号隔开")):
    mor_ids = ids.split(",")
    deleted_ids = []
    for mor_id in mor_ids:
        license_obj = await mor_controller.get(id=int(mor_id))
        await license_obj.delete()
        deleted_ids.append(int(mor_id))
    return Success(msg="Deleted Successfully", data={"deleted_ids": deleted_ids})
