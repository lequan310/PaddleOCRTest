import paddle
import paddle.device
import numpy as np
import time
from paddleocr import PaddleOCR
from core.config import get_logger


logger = get_logger(__name__)


class OCR:
    def __init__(self):
        logger.info(f"Paddle device: {paddle.device.get_device()}")
        use_gpu = paddle.device.is_compiled_with_cuda()
        self._model = PaddleOCR(
            use_angle_cls=True, lang="en", use_gpu=use_gpu, show_log=False
        )
        logger.info("PaddleOCR model loaded successfully.")

    def ocr(self, img: np.ndarray, show_log: bool = True) -> list:
        logger.disabled = not show_log
        logger.debug("Performing OCR on the image.")
        start_time = time.time()
        ocr_result = self._model.ocr(img)
        end_time = time.time()
        logger.debug(f"OCR time: {end_time - start_time} ms")
        result = [
            {"text": detection[1][0], "confidence": detection[1][1]}
            for detection in ocr_result[0]
        ]
        return result
