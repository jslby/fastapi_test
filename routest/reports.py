from fastapi import APIRoutes, UploadFile, File
from fastapi.responses import Response
from typing import List
from services.merger import merge_reports

router = APIRoutes()

@router.post("/merge")
async def merge(
    fb_files: List[UploadFile] = File(...),
    kt_files: UploadFile = File(...)
):
    fb_bytes = [await f.read() for f in fb_files]
    kt_bytes = await kt_files.read()

    result = merge_reports(fb_bytes, kt_bytes)

    return Response(
        content = result,
        media_type = "text/csv",
        headers = {"Content-Disposition": "attachment; filename=result.csv"}
    )