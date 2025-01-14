import httpx
from core.config import os


class OCRService:
    def __init__(self):
        self._ocr_api = os.getenv("OCR_API", "http://localhost:8080")

    async def ocr(self, base64_img: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{self._ocr_api}/ocr/single", json=base64_img
            )
            return response.json()

    async def batch_ocr(self, base64_imgs: list[str]):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{self._ocr_api}/ocr/batch", json=base64_imgs
            )
            return response.json()
