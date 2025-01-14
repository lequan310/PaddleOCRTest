from typing import Annotated
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from ray import serve
from ray.serve.handle import DeploymentHandle
from ray.serve.schema import LoggingConfig
from paddle_ocr import OCRService

app = FastAPI(title="Model Serving API")


@serve.deployment(
    num_replicas=1,
    logging_config=LoggingConfig(log_level="INFO", logs_dir="./logs"),
    health_check_period_s=10,
    health_check_timeout_s=30,
)
@serve.ingress(app)
class APIIngress:
    def __init__(self, ocr_handle: DeploymentHandle):
        # Add more models here if needed.
        self.ocr_handle = ocr_handle

    @app.post("/ocr/single")
    async def ocr(self, base64_img: Annotated[str, Body()]):
        result = await self.ocr_handle.remote(base64_img)
        return result

    @app.post("/ocr/batch")
    async def ocr(self, base64_imgs: Annotated[list[str], Body()]):
        results = [
            await self.ocr_handle.remote(base64_img) for base64_img in base64_imgs
        ]
        return {"result": results}


ocr_service = OCRService.bind()
entrypoint = APIIngress.bind(ocr_service)


if __name__ == "__main__":
    serve.run(entrypoint)
