import json
from fastapi import APIRouter, Depends
from fastapi import UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse
from src.schemas.image_segmentation import ImageSegmentation
from src.schemas.image_rem_items import ImageRemoveItems
from src.controllers.image_seg_controller import get_image_obj_segments, get_image_obj_segments_data, image_remove_items_from_list
from src.controllers.status_controller import get_service_status
from src.controllers.reports_controller import get_reports
from src.models.object_segmentation import ObjectSegmentator
from src.services.csv_service import CSVService
from src.schemas.status import Status
from src.models.segmentation_inst_data import SegmentationInstanceData
from pydantic import ValidationError
from fastapi import HTTPException, status
from src.schemas.image_rem_items import Item


def get_object_segmentator():
    return ObjectSegmentator()

def get_csv_service():
    return CSVService()

router = APIRouter()


@router.get("/status")
def root(predictor_model: ObjectSegmentator = Depends(get_object_segmentator)) -> Status:
    return get_service_status(predictor_model)

@router.post("/predict-image", response_class=FileResponse)
def predict(image_segmentation: ImageSegmentation = Depends(), predictor: ObjectSegmentator = Depends(get_object_segmentator), csv_service: CSVService = Depends(get_csv_service)) -> FileResponse:
    return get_image_obj_segments(
        image_segmentation.image_file, image_segmentation.confidence_threshold, predictor, csv_service
    )
    
@router.post("/predict-data")
def predict_data(image_segmentation: ImageSegmentation = Depends(), predictor: ObjectSegmentator = Depends(get_object_segmentator), csv_service: CSVService = Depends(get_csv_service)) -> list[SegmentationInstanceData]:
    return get_image_obj_segments_data(
        image_segmentation.image_file, image_segmentation.confidence_threshold, predictor, csv_service
    )

@router.post("/remove-items-image", response_class=FileResponse)
def remove_items(image_file: UploadFile = File(..., description="Image file"), confidence_threshold: float = Form(0.5), items = Form([]), 
predictor: ObjectSegmentator = Depends(get_object_segmentator), csv_service: CSVService = Depends(get_csv_service)) -> FileResponse:
    
    # Validate the items array as a JSON
    try:
        json_items = json.loads(items)
        items = [Item(**item) for item in json_items]
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    return image_remove_items_from_list(
        image_file, confidence_threshold, items, predictor, csv_service
    )

@router.get("/reports", response_class=StreamingResponse)
def reports(csv_service: CSVService = Depends(get_csv_service)) -> StreamingResponse:
    return get_reports(csv_service)