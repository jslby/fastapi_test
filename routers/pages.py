from fastapi import APIRouter
from fastapo.responses import FileResponses

router = APIRouter()

@router.get("/")
async def index():
    return FileResponses()