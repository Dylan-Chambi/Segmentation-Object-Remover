# /src/routers/image_prediction.py

from fastapi import APIRouter, HTTPException, Depends, status
from src.schemas.ImageSegmentation import ImageSegmentation
from src.services.image_seg import get_image_obj_segments, get_image_obj_segments_data
from src.services.status import get_service_status
from src.models.ObjectSegmentator import ObjectSegmentator


def get_object_segmentator():
    return ObjectSegmentator()

router = APIRouter()


@router.get("/status")
def root(predictor_model: ObjectSegmentator = Depends(get_object_segmentator)):
    return get_service_status(predictor_model)

@router.post("/predict-image")
def predict(image_segmentation: ImageSegmentation = Depends(), predictor: ObjectSegmentator = Depends(get_object_segmentator)):
    return get_image_obj_segments(
        image_segmentation.image_file, image_segmentation.confidence_threshold, predictor
    )
    
@router.post("/predict-data")
def predict_data(image_segmentation: ImageSegmentation = Depends(), predictor: ObjectSegmentator = Depends(get_object_segmentator)):
    return get_image_obj_segments_data(
        image_segmentation.image_file, image_segmentation.confidence_threshold, predictor
    )


@router.get("/reports")
def reports():
    return {"message": "Hello World from image_prediction_router"}