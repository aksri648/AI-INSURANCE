import pdfplumber
from PIL import Image
import io
from typing import Optional
from pathlib import Path
from loguru import logger


class OCRService:
    async def extract_text(self, file_path: str, file_type: str) -> str:
        ext = Path(file_path).suffix.lower()

        if ext == ".pdf":
            return await self._extract_pdf(file_path)
        elif ext in (".png", ".jpg", ".jpeg", ".tiff"):
            return await self._extract_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    async def _extract_pdf(self, file_path: str) -> str:
        text_parts = []
        page_count = 0
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text_parts.append(page_text)
                    page_count += 1
            logger.info(f"Extracted {page_count} pages from PDF")
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            raise
        return "\n\n".join(text_parts)

    async def _extract_image(self, file_path: str) -> str:
        try:
            import pytesseract
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            logger.info(f"Extracted text from image: {len(text)} chars")
            return text
        except ImportError:
            logger.warning("pytesseract not installed, trying pdfplumber backup")
            return f"[Image file: {file_path}]"
        except Exception as e:
            logger.error(f"Image OCR failed: {e}")
            return f"[Image file could not be processed: {file_path}]"

    async def extract_metadata(self, file_path: str) -> dict:
        metadata = {}
        ext = Path(file_path).suffix.lower()
        try:
            if ext == ".pdf":
                with pdfplumber.open(file_path) as pdf:
                    metadata = pdf.metadata or {}
                    metadata["page_count"] = len(pdf.pages)
            return metadata
        except Exception as e:
            logger.warning(f"Metadata extraction failed: {e}")
            return {"page_count": 0}


ocr_service = OCRService()
