from pydantic import BaseModel

class SegmentationInstanceData(BaseModel):
    class_name: str
    seg_mask_polygon: list[list[float]]
    score: float
