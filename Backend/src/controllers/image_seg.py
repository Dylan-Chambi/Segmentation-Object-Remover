from fastapi import File, UploadFile, HTTPException, status, Response, Depends
from src.models.ObjectSegmentator import ObjectSegmentator
from src.models.SegmentationData import SegmentationInstanceData
import io
from PIL import Image
import numpy as np
import time
from src.services.CSVService import CSVService, CSVItem
from src.utils.functions import human_size
from src.models.ServiceType import ServiceType

def get_image_obj_segments(img_file: UploadFile, confidence: float, predictor: ObjectSegmentator, csv_service: CSVService) -> Response:
    # Start counting the time
    start = time.time()
    # Read the image file into a stream
    img_stream = io.BytesIO(img_file.file.read())

    # Check if the content type is an image
    if img_file.content_type.split("/")[0] != "image":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Not an image"
        )

    # Convert to a Pillow image
    img_obj = Image.open(img_stream)

    # Convert to a NumPy array
    img_array = np.array(img_obj)

    # Perform image segmentation using the provided predictor
    seg_img_pil, _ = predictor.segment_image(img_array, confidence)

    # Save the segmented image to a stream in JPEG format
    img_stream = io.BytesIO()
    seg_img_pil.save(img_stream, format="JPEG")
    img_stream.seek(0)


    # End counting the time
    end = time.time()

    # Register into 
    csv_service.write_csv(
        CSVItem(
            file_name=img_file.filename,
            image_size=human_size(len(img_stream.getbuffer())),
            prediction_type=ServiceType.IMAGE_SEGMENTATION,
            datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            execution_time=end - start,
            model=predictor.model_name,
            confidence_threshold=confidence
        )
    )


    # Return the segmented image as a FastAPI Response
    return Response(content=img_stream.read(), media_type="image/jpeg")


def get_image_obj_segments_data(img_file: UploadFile, confidence: float, predictor: ObjectSegmentator, csv_service: CSVService) -> list[SegmentationInstanceData]:
    # Start counting the time
    start = time.time()
    # Read the image file into a stream
    img_stream = io.BytesIO(img_file.file.read())

    # Check if the content type is an image
    if img_file.content_type.split("/")[0] != "image":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Not an image"
        )

    # Convert to a Pillow image
    img_obj = Image.open(img_stream)

    # Convert to a NumPy array
    img_array = np.array(img_obj)

    # Perform image segmentation using the provided predictor
    _, seg_data = predictor.segment_image(img_array, confidence)

    # End counting the time
    end = time.time()

    # Register into CSV
    csv_service.write_csv(
        CSVItem(
            file_name=img_file.filename,
            image_size=human_size(len(img_stream.getbuffer())),
            prediction_type=ServiceType.IMAGE_DATA_SEG,
            datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            execution_time=end - start,
            model=predictor.model_name,
            confidence_threshold=confidence
        )
    )

    # Return the segmented image data
    return seg_data
