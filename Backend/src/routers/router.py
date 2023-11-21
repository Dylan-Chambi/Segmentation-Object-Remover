# /src/routers/image_prediction.py

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from src.schemas.image_segmentation import ImageSegmentation
from src.controllers.image_seg_controller import get_image_obj_segments, get_image_obj_segments_data
from src.controllers.status_controller import get_service_status
from src.controllers.reports_controller import get_reports
from src.models.object_segmentation import ObjectSegmentator
from src.services.csv_service import CSVService


def get_object_segmentator():
    return ObjectSegmentator()

def get_csv_service():
    return CSVService()

router = APIRouter()


@router.get("/status")
def root(predictor_model: ObjectSegmentator = Depends(get_object_segmentator)):
    return get_service_status(predictor_model)

@router.post("/predict-image")
def predict(image_segmentation: ImageSegmentation = Depends(), predictor: ObjectSegmentator = Depends(get_object_segmentator), csv_service: CSVService = Depends(get_csv_service)):
    return get_image_obj_segments(
        image_segmentation.image_file, image_segmentation.confidence_threshold, predictor, csv_service
    )
    
@router.post("/predict-data")
def predict_data(image_segmentation: ImageSegmentation = Depends(), predictor: ObjectSegmentator = Depends(get_object_segmentator), csv_service: CSVService = Depends(get_csv_service)):
    return get_image_obj_segments_data(
        image_segmentation.image_file, image_segmentation.confidence_threshold, predictor, csv_service
    )


@router.get("/reports")
def reports(csv_service: CSVService = Depends(get_csv_service)) -> StreamingResponse:
    return get_reports(csv_service)