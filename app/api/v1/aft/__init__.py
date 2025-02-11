from fastapi import APIRouter
from .aft import router

router_aft = APIRouter()
router_aft.include_router(router)
