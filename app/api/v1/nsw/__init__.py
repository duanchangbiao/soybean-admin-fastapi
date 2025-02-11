from fastapi import APIRouter
from .nsw import router

router_nsw = APIRouter()
router_nsw.include_router(router)
