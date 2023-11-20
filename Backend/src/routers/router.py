# /src/routers/image_prediction.py

from fastapi import APIRouter, HTTPException, Depends, status
from src.schemas.ImageSegmentation import ImageSegmentation
from src.services.image_seg import get_image_obj_segments
from src.models.ObjectSegmentator import ObjectSegmentator


def get_object_segmentator():
    return ObjectSegmentator()

router = APIRouter()


@router.get("/status")
def root():
    return {"message": "Hello World from image_prediction_router"}

@router.post("/predict")
def predict(image_segmentation: ImageSegmentation = Depends(), predictor: ObjectSegmentator = Depends(get_object_segmentator)):
    try:
        return get_image_obj_segments(
            image_segmentation.image_file, image_segmentation.confidence_threshold, predictor
        )
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/reports")
def reports():
    return {"message": "Hello World from image_prediction_router"}