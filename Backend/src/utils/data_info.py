from src.schemas.status_endpoints import StatusEndpoints
from src.models.http_method import HTTPMethod

MODEL_DESCRIPTION = "This is a web service that allows you to segment objects in images using an Image Segmentation model like YOLOv8."

SERVICE_ENDPOINTS = [
    StatusEndpoints(
                    path="/status",
                    description="Get the status of the service",
                    method=HTTPMethod.GET,
                ),
                StatusEndpoints(
                    path="/predict-image",
                    description="Get the segmentation of an image",
                    method=HTTPMethod.POST,
                ),
                StatusEndpoints(
                    path="/predict-data",
                    description="Get the segmentation of an image",
                    method=HTTPMethod.POST
                ),
                StatusEndpoints(
                    path="/reports",
                    description="Get the reports of the service",
                    method=HTTPMethod.GET
                )
]