from fastapi import APIRouter

from app.core.dependency import DependPermission
from .license import router

from .license import router as license_router

router_license = APIRouter()

router_license.include_router(license_router, tags=["许可证查询管理"], dependencies=[DependPermission])
