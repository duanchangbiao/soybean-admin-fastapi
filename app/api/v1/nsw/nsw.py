from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.api.v1.utils import insert_log
from app.controllers import user_controller
from app.controllers.nsw import nsw_controller
from app.core.ctx import CTX_USER_ID
from app.models.system import LogType, LogDetailType, Role
from app.models.system.business import Account
from app.schemas.base import Success, SuccessExtra
from app.schemas.nsw import NswCreate, NswUpdate

router = APIRouter()


@router.post("/list", summary="查看Nsw列表")
async def _(
        current: int = Query(1, description="页码"),
        size: int = Query(10, description="每页数量"),
        applyNumber: str = Query(None, description="申请id"),
        applyStatus: str = Query(None, description="申请状态"),
        remark: str = Query(None, description="备注"),
        accountNumber: str = Query(None, description="昵称"),
):
    q = Q()
    if accountNumber:
        _by_account: Account = await Account.get_or_none(account_number=accountNumber)
        q &= Q(by_nsw_account=_by_account)
    if applyNumber:
        q &= Q(apply_number__contains=applyNumber)
    if applyStatus:
        q &= Q(apply_status__contains=applyStatus)
    if remark:
        q &= Q(remark__contains=remark)
    user_id = CTX_USER_ID.get()  # 从请求的token获取用户id
    user_obj = await user_controller.get(id=user_id)
    user_role_objs: list[Role] = await user_obj.by_user_roles
    user_role_codes = [role_obj.role_code for role_obj in user_role_objs]
    if "R_SUPER" not in user_role_codes:  # 超级管理员具有所有权限
        q &= Q(create_by=user_obj.nick_name)

    total, aft_objs = await nsw_controller.list(page=current, page_size=size, search=q,
                                                order=["-sort", "-remark", "-ctime", "-mtime", "id"])
    records = []
    for aft_obj in aft_objs:
        record = await aft_obj.to_dict(exclude_fields=["by_nsw_account"])
        await aft_obj.fetch_related("by_nsw_account")
        account = await aft_obj.by_nsw_account
        if len(account) != 0:
            record.update({"nickName": account[0].nickname})
            record.update({"accountNumber": account[0].account_number})
        records.append(record)
    data = {"records": records}
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetList, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.get("/get/{nsw_id}", summary="查看nsw")
async def get_user(nsw_id: int):
    user_obj = await nsw_controller.get(id=nsw_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetOne, by_user_id=0)
    return Success(data=await user_obj.to_dict(exclude_fields=["by_nsw_account"]))


@router.post("/add", summary="创建nsw")
async def _(nsw_in: NswCreate):
    if not nsw_in.by_nsw_account:
        return Success(code="4090", msg="The aft must have account number that exists.")
    account = await nsw_controller.get_by_account_number(account_number=nsw_in.by_nsw_account)
    if not account:
        return Success(code="4090", msg="The account number is not exists.")
    new_aft = await nsw_controller.create(obj_in=nsw_in, exclude={"by_nsw_account"})
    await nsw_controller.update_nsw_account(new_aft, nsw_in.by_nsw_account)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserCreateOne, by_user_id=0)
    return Success(msg="Created Successfully", data={"created_id": new_aft.id})


@router.patch("/update/{nsw_id}", summary="更新aft")
async def _(nsw_id: int, nsw_in: NswUpdate):
    if not nsw_in.by_nsw_account:
        return Success(code="4090", msg="The aft must have account number that exists.")
    account = await nsw_controller.get_by_account_number(account_number=nsw_in.by_nsw_account)
    if not account:
        return Success(code="4090", msg="The account number is not exists.")
    mor = await nsw_controller.update(id=nsw_id, obj_in=nsw_in, exclude={"by_nsw_account"})
    await nsw_controller.update_nsw_account(mor, nsw_in.by_nsw_account)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserUpdateOne, by_user_id=0)
    return Success(msg="Updated Successfully", data={"updated_id": nsw_id})


@router.delete("/delete/{nsw_id}", summary="删除mor")
async def _(nsw_id: int):
    await nsw_controller.remove(id=nsw_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserDeleteOne, by_user_id=0)
    return Success(msg="Deleted Successfully", data={"deleted_id": nsw_id})


@router.delete("/batch", summary="批量删除mor")
async def _(ids: str = Query(..., description="删除aft列表, 用逗号隔开")):
    mor_ids = ids.split(",")
    deleted_ids = []
    for mor_id in mor_ids:
        license_obj = await nsw_controller.get(id=int(mor_id))
        await license_obj.delete()
        deleted_ids.append(int(mor_id))
    return Success(msg="Deleted Successfully", data={"deleted_ids": deleted_ids})
