from fastapi import File, UploadFile
from typing import Optional
from pydantic import BaseModel, Field

class ImageSegmentation(BaseModel):
    image_file: UploadFile = File(...)
    confidence_threshold: Optional[float] = 0.5