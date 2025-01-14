import base64
import numpy as np
from io import BytesIO
from PIL import Image
from paddleocr import PaddleOCR
from ray import serve
from ray.serve.schema import LoggingConfig
from logging import getLogger

logger = getLogger("ray.serve")


@serve.deployment(
    ray_actor_options={"num_gpus": 0.5, "num_cpus": 0.5},
    autoscaling_config={"min_replicas": 1, "max_replicas": 2},
    logging_config=LoggingConfig(log_level="INFO", logs_dir="./logs"),
    health_check_period_s=10,
    health_check_timeout_s=30,
)
class OCRService:
    def __init__(self):
        self._model = PaddleOCR(
            use_angle_cls=True, lang="en", use_gpu=True, show_log=False
        )

    def _base64_to_numpy(self, base64_img: str):
        img = base64.b64decode(base64_img)
        with BytesIO(img) as img_buffer, Image.open(img_buffer) as img:
            return np.array(img)

    def __call__(self, base64_img: str):
        try:
            np_arr = self._base64_to_numpy(base64_img)
            ocr_result = self._model.ocr(np_arr)[0]
            return {"result": ocr_result}
        except Exception as e:
            logger.exception(e)
            return {"result": []}
