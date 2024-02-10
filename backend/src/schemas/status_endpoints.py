from typing import Optional
from pydantic import BaseModel
from src.models.http_method import HTTPMethod

class StatusEndpoints(BaseModel):
    path: str
    description: Optional[str] = None
    method: HTTPMethod
