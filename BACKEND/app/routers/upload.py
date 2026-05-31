from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.middleware.clerk import get_current_user
from app.models import User, Policy
from app.database import async_session
from app.services.storage import storage
from sqlalchemy import select
from pathlib import Path

router = APIRouter(prefix="/api/files", tags=["Files"])


@router.get("/{filename}")
async def get_file(filename: str):
    file_path = Path(storage.upload_dir) / "policies" / filename
    if not file_path.exists():
        for subdir in ["policies"]:
            candidate = Path(storage.upload_dir) / subdir / filename
            if candidate.exists():
                file_path = candidate
                break
        else:
            raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(str(file_path))
