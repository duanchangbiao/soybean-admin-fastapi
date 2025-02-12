from fastapi import APIRouter
from .dict import router

router_dict = APIRouter()
router_dict.include_router(router)
