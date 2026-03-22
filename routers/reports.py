from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from typing import List, Annotated
from services.merger import merge_reports

router = APIRouter()

@router.post("/merge")
async def merge(
    fb_files: List[Annotated[UploadFile, File()]],
    kt_files: Annotated[UploadFile, File()]
):
    fb_bytes = [await f.read() for f in fb_files]
    kt_bytes = await kt_files.read()

    result = merge_reports(fb_bytes, kt_bytes)

    return Response(
        content = result,
        media_type = "text/csv",
        headers = {"Content-Disposition": "attachment; filename=result.csv"}
    )