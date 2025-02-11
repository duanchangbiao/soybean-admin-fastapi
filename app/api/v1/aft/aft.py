from fastapi import APIRouter, FastAPI

router = APIRouter()


@router.get("/aft/list")
async def _():
    return {"message": "Hello World"}
