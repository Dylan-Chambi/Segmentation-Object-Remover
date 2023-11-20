# /src/routers/image_prediction.py

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/status")
def root():
    return {"message": "Hello World from image_prediction_router"}


@router.post("/predict")
def predict():
    return {"message": "Hello World from image_prediction_router"}


@router.get("/reports")
def reports():
    return {"message": "Hello World from image_prediction_router"}