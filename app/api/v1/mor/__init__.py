from fastapi import APIRouter
from .mor import router

router_mor = APIRouter()
router_mor.include_router(router)
