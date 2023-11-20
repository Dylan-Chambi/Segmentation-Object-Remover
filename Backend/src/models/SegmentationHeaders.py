from uuid import UUID
from pydantic import BaseModel

class SegmentationHeaders(BaseModel):
    id: UUID
    seg_classes: list[str]

    def __init__(self, id: UUID, seg_classes: list[str]):
        self.id = id
        self.seg_classes = seg_classes
