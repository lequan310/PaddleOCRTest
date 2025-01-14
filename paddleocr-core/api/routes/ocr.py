import base64
import pymupdf
from fastapi import APIRouter, File, UploadFile, HTTPException
from core.ocr import OCRService
from core.config import get_logger

logger = get_logger(__name__)
ocr_service = OCRService()
router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.post("/upload")
async def ocr_file(file: UploadFile = File(...)):
    try:
        if file.content_type.startswith("image/"):
            # Read the file as bytes
            image_data = await file.read()
            base64_img = base64.b64encode(image_data).decode("utf-8")

            # Perform OCR
            result = await ocr_service.ocr(base64_img=base64_img)
            return result
        elif file.content_type == "application/pdf":
            # Read the file as bytes
            file_data = await file.read()
            # Extract images from PDF
            with pymupdf.open(stream=file_data, filetype="pdf") as pdf_document:
                images = [page.get_pixmap() for page in pdf_document]

            # Convert images to base64
            base64_imgs = [
                base64.b64encode(image.tobytes()).decode("utf-8") for image in images
            ]
            result = await ocr_service.batch_ocr(base64_imgs=base64_imgs)
            return result
        else:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported media type {file.content_type}. Only images and PDFs are supported.",
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        await file.close()
