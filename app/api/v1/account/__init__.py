from fastapi import APIRouter
from .account import router

router_account = APIRouter()
router_account.include_router(router)
