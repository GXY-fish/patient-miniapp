from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import get_settings
from app.schemas.common import UploadResponse

router = APIRouter(prefix="/uploads", tags=["uploads"])

settings = get_settings()
upload_root = Path(settings.upload_dir).resolve()
upload_root.mkdir(parents=True, exist_ok=True)


@router.post("", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    target_path = upload_root / file.filename
    content = await file.read()
    target_path.write_bytes(content)

    return UploadResponse(
        filename=file.filename,
        path=f"/uploads/{file.filename}",
        size=len(content),
    )
