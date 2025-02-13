from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.api.v1.utils import insert_log
from app.controllers import user_controller
from app.controllers.account import account_controller
from app.core.ctx import CTX_USER_ID
from app.models.system import LogType, LogDetailType, Role
from app.models.system.business import Dict
from app.schemas.account import AccountCreate
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

    user_id = CTX_USER_ID.get()  # 从请求的token获取用户id
    user_obj = await user_controller.get(id=user_id)
    user_role_objs: list[Role] = await user_obj.by_user_roles
    user_role_codes = [role_obj.role_code for role_obj in user_role_objs]
    if "R_SUPER" not in user_role_codes:  # 超级管理员具有所有权限
        q &= Q(create_by=user_obj.nick_name)
    total, account_objs = await account_controller.list(page=current, page_size=size, search=q,
                                                        order=['-ctime'])
    records = []
    for account_obj in account_objs:
        record = await account_obj.to_dict(exclude_fields=["by_account_dict"])
        await account_obj.fetch_related("by_account_dict")
        account_monitor_list = [by_account_dict.id for by_account_dict in account_obj.by_account_dict]
        record.update({"accountMonitorList": account_monitor_list})
        records.append(record)
    data = {"records": records}
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetList, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.get("/get/{account_id}", summary="查看account")
async def get_user(account_id: int):
    user_obj = await account_controller.get(id=account_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetOne, by_user_id=0)
    return Success(data=await user_obj.to_dict(exclude_fields=["by_mor_account"]))


@router.post("/add", summary="创建account")
async def _(account_in: AccountCreate):
    if not account_in.by_account_modules:
        return Success(code="4090", msg="The aft must have account number that exists.")
    user_id = CTX_USER_ID.get()  # 从请求的token获取用户id
    user_obj = await user_controller.get(id=user_id)
    account_in.create_by = user_obj.nick_name
    new_account = await account_controller.create(obj_in=account_in, exclude={"by_account_modules"})
    await account_controller.update_dict_by_value(new_account, account_in.by_account_modules)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserCreateOne, by_user_id=0)
    return Success(msg="Created Successfully", data={"created_id": new_account.id})


@router.patch("/update/{account_id}", summary="更新account")
async def _(account_id: int, account_in: AccountCreate):
    user_id = CTX_USER_ID.get()  # 从请求的token获取用户id
    user_obj = await user_controller.get(id=user_id)
    account_in.update_by = user_obj.nick_name
    account = await account_controller.update(id=account_id, obj_in=account_in, exclude={"by_account_modules"})
    if account_in.by_account_modules is not None:
        await account_controller.update_dict_by_value(account, account_in.by_account_modules)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserUpdateOne, by_user_id=0)
    return Success(msg="Updated Successfully", data={"updated_id": account_id})


@router.delete("/delete/{account_id}", summary="删除account")
async def _(account_id: int):
    await account_controller.remove(id=account_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserDeleteOne, by_user_id=0)
    return Success(msg="Deleted Successfully")


@router.delete("/batch", summary="批量删除account")
async def _(ids: str = Query(..., description="删除account列表, 用逗号隔开")):
    deleted_ids = []
    for account_id in ids:
        account_obj = await account_controller.get(id=int(account_id))
        await account_obj.delete()
        deleted_ids.append(int(account_id))
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserDeleteOne, by_user_id=0)
    return Success(msg="Deleted Successfully", data={"deleted_id": ids})
