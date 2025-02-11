from fastapi import APIRouter, FastAPI, Query
from tortoise.expressions import Q

from app.api.v1.utils import insert_log
from app.controllers.aft import aft_controller
from app.models.system import LogType, LogDetailType, Account
from app.schemas.aft import AftSearch, AftCreate, AftUpdate
from app.schemas.base import SuccessExtra, Success, CommonIds

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
            q &= Q(by_aft_account=_by_account)
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
        await aft_obj.fetch_related("by_aft_account")
        account = await aft_obj.by_aft_account
        if len(account) != 0:
            record.update({"nickName": account[0].nickname})
            record.update({"accountNumber": account[0].account_number})
        records.append(record)
    data = {"records": records}
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetList, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.get("/get/{aft_id}", summary="查看aft")
async def get_user(aft_id: int):
    user_obj = await aft_controller.get(id=aft_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetOne, by_user_id=0)
    return Success(data=await user_obj.to_dict(exclude_fields=["password"]))


@router.post("/add", summary="创建aft")
async def _(aft_in: AftCreate):
    new_aft = await aft_controller.create(obj_in=aft_in, exclude={"by_aft_account"})
    if not aft_in.by_aft_account:
        return Success(code="4090", msg="The user must have at least one role that exists.")
    await aft_controller.update_aft_account(new_aft, aft_in.by_aft_account)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserCreateOne, by_user_id=0)
    return Success(msg="Created Successfully", data={"created_id": new_aft.id})


@router.patch("/update/{aft_id}", summary="更新aft")
async def _(aft_id: int, aft_in: AftUpdate):
    aft = await aft_controller.update(id=aft_id, obj_in=aft_in, exclude={"by_aft_account"})
    if not aft_in.by_aft_account:
        return Success(code="4090", msg="The user must have at least one role that exists.")

    await aft_controller.update_aft_account(aft, aft_in.by_aft_account)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserUpdateOne, by_user_id=0)
    return Success(msg="Updated Successfully", data={"updated_id": aft_id})


@router.delete("/delete/{aft_id}", summary="删除aft")
async def _(aft_id: int):
    await aft_controller.remove(id=aft_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserDeleteOne, by_user_id=0)
    return Success(msg="Deleted Successfully", data={"deleted_id": aft_id})


@router.delete("/batch", summary="批量删除aft")
async def _(ids: str = Query(..., description="删除aft列表, 用逗号隔开")):
    license_ids = ids.split(",")
    deleted_ids = []
    for license_id in license_ids:
        license_obj = await aft_controller.get(id=int(license_id))
        await license_obj.delete()
        deleted_ids.append(int(license_id))
    return Success(msg="Deleted Successfully", data={"deleted_ids": deleted_ids})
