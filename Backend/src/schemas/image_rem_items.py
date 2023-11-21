from fastapi import File, UploadFile
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import UploadFile, Form

class Item(BaseModel):
    class_name: str
    instance_id: int

class ImageRemoveItems(BaseModel):
    image_file: UploadFile = File(...)
    confidence_threshold: Optional[float] = Form(0.5)
    items: str = Form(['{ "class_name": "person", "instance_id": 1 }'])