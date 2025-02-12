from fastapi import APIRouter

from .auth import router_auth
from .license import router_license
from .route import router_route
from .system_manage import router_system_manage
from .aft import router_aft
from .mor import router_mor
from .nsw import router_nsw
from .account import router_account
from .dict import router_dict

v1_router = APIRouter()

v1_router.include_router(router_auth, prefix="/auth", tags=["权限认证"])
v1_router.include_router(router_route, prefix="/route", tags=["路由管理"])
v1_router.include_router(router_system_manage, prefix="/system-manage", tags=["系统管理"])
v1_router.include_router(router_license, prefix="/license", tags=["公司信息查询"])
v1_router.include_router(router_aft, prefix="/aft", tags=["aft affa 信息查询"])
v1_router.include_router(router_mor, prefix="/mor", tags=["mor9 mor5 信息查询"])
v1_router.include_router(router_nsw, prefix="/nsw", tags=["nsw 信息查询"])
v1_router.include_router(router_account, prefix="/account", tags=["账户信息查询"])
v1_router.include_router(router_dict, prefix="/dict", tags=["字典信息查询"])
