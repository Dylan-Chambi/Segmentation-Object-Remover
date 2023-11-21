from pydantic import BaseModel

class SegmentationInstanceData(BaseModel):
    class_name: str
    instance_id: int
    seg_mask_polygon: list[list[float]]
    score: float
