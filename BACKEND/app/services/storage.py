import aiofiles
import os
import uuid
from pathlib import Path
from app.config import settings
from typing import BinaryIO, Optional
from loguru import logger


class StorageService:
    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, file: BinaryIO, filename: str, subdir: str = "policies") -> str:
        file_id = str(uuid.uuid4())
        ext = Path(filename).suffix.lower()
        safe_name = f"{file_id}{ext}"
        dest_dir = self.upload_dir / subdir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / safe_name

        async with aiofiles.open(str(dest_path), "wb") as f:
            content = file.read()
            await f.write(content)

        logger.info(f"Saved file to {dest_path}")
        return str(dest_path)

    async def delete(self, file_path: str) -> bool:
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
        return False

    async def get_path(self, file_path: str) -> Optional[str]:
        path = Path(file_path)
        if path.exists():
            return str(path)
        return None

    async def get_public_url(self, file_path: str) -> str:
        return f"/api/files/{Path(file_path).name}"


storage = StorageService()
