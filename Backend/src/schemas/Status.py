from typing import Optional
from pydantic import BaseModel
from src.schemas.status_endpoints import StatusEndpoints

class Status(BaseModel):
    yolo_version: str
    description: Optional[str] = None
    num_layers: Optional[int] = None
    num_parameters: Optional[int] = None
    gflops: Optional[float] = None
    endpoints: list[StatusEndpoints] = None
