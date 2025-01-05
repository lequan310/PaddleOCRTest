import numpy as np
from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
from io import BytesIO
from core.ocr import OCR
from core.config import get_logger

logger = get_logger(__name__)
ocr_model = OCR()
router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.post("/upload")
async def ocr_file(file: UploadFile = File(...)):
    try:
        if file.content_type.startswith("image/"):
            # Read the file as bytes
            image_data = await file.read()

            # Convert to NumPy ndarray using Pillow
            with BytesIO(image_data) as bytes_io, Image.open(bytes_io) as img:
                img_array = np.array(img)

            # Perform OCR
            result = ocr_model.ocr(img=img_array, show_log=True)
            return {"result": result}
        else:
            raise HTTPException(
                status_code=415, detail=f"Unsupported media type: {file.filename}"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        await file.close()


@router.post("/batch_upload")
async def ocr_batch_files(files: list[UploadFile] = File(...)):
    try:
        results = []
        for file in files:
            if file.content_type.startswith("image/"):
                # Read the file as bytes
                image_data = await file.read()

                # Convert to NumPy ndarray using Pillow
                with BytesIO(image_data) as bytes_io, Image.open(bytes_io) as img:
                    img_array = np.array(img)

                # Perform OCR
                result = ocr_model.ocr(img=img_array)
                results.append(result)
            else:
                raise HTTPException(
                    status_code=415, detail=f"Unsupported media type: {file.filename}"
                )
        return {"results": results}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        for file in files:
            await file.close()
