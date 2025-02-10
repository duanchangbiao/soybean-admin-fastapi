from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.api.v1.utils import insert_log
from app.controllers import license_controller
from app.models.system import LogType, LogDetailType
from app.schemas.base import SuccessExtra, Success, CommonIds
from app.schemas.license import LicenseCreate

router = APIRouter()


@router.post("/list", summary="查看公司详情列表")
async def _(
        current: int = Query(1, description="页码"),
        size: int = Query(10, description="每页数量"),
        licenseId: str = Query(None, description="角色名称"),
        companyName: str = Query(None, description="角色编码"),
        taxIdentificationNumber: str = Query(None, description="用户状态")
):
    q = Q()
    if licenseId:
        q &= Q(license_id__contains=licenseId)
    if companyName:
        q &= Q(company_name__contains=companyName)
    if taxIdentificationNumber:
        q &= Q(tax_identification_number__contains=taxIdentificationNumber)

    total, license_objs = await license_controller.list(page=current, page_size=size, search=q, order=["id"])
    records = [await license_obj.to_dict() for license_obj in license_objs]  # exclude_fields=["role_desc"]
    data = {"records": records}
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.RoleGetList, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.get("/{license_id}", summary="查看许可证id")
async def get_user(user_id: int):
    license_obj = await license_controller.get(id=user_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserGetOne, by_user_id=0)
    return Success(data=await license_obj.to_dict())


@router.post("/add", summary="创建许可信息")
async def _(license_in: LicenseCreate):
    license = await license_controller.model.exists(license_id=license_in.role_code)
    if license:
        return Success(code="4090", msg="The license with this code already exists in the system.")

    new_license = await license_controller.create(obj_in=license_in)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserCreateOne, by_user_id=0)
    return Success(msg="Created Successfully", data={"created_id": new_license.id})


@router.patch("/update/{license_id}", summary="更新许可证")
async def _(license_id: int, license_in: LicenseCreate):
    user = await license_controller.update(license_id=license_id, obj_in=license_in)
    if not license_in.by_user_role_code_list:
        return Success(code="4090", msg="The license must exists.")

    await license_controller.update_roles_by_code(user, license_in.by_user_role_code_list)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserUpdateOne, by_user_id=0)
    return Success(msg="Updated Successfully", data={"updated_id": license_id})


@router.delete("/delete/{user_id}", summary="删除许可证")
async def _(user_id: int):
    await license_controller.remove(id=user_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserDeleteOne, by_user_id=0)
    return Success(msg="Deleted Successfully", data={"deleted_id": user_id})


@router.delete("/delete/batch", summary="批量删除用户")
async def _(obj_in: CommonIds):
    deleted_ids = []
    for license_id in obj_in.ids:
        license_obj = await license_controller.get(id=int(license_id))
        await license_obj.delete()
        deleted_ids.append(int(license_id))

    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.UserBatchDeleteOne, by_user_id=0)
    return Success(msg="Deleted Successfully", data={"deleted_ids": deleted_ids})
