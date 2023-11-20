# /src/routers/image_prediction.py

from fastapi import APIRouter, HTTPException, Depends
from src.schemas.ImageSegmentation import ImageSegmentation
from src.services.image_seg import get_image_obj_segments

router = APIRouter()


@router.get("/status")
def root():
    return {"message": "Hello World from image_prediction_router"}


@router.post("/predict")
def predict(image_segmentation: ImageSegmentation = Depends()):
    try:
        return get_image_obj_segments(
            image_segmentation.image_file, image_segmentation.confidence_threshold
        )
    except Exception as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.get("/reports")
def reports():
    return {"message": "Hello World from image_prediction_router"}