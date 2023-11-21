from fastapi import UploadFile, HTTPException, status, Response
from src.models.object_segmentation import ObjectSegmentator
from src.models.segmentation_inst_data import SegmentationInstanceData
import io
from PIL import Image
import numpy as np
import time
from src.services.csv_service import CSVService, CSVItem
from src.utils.functions import human_size
from src.models.service_type import ServiceType
from src.middlewares.image_seg_middleware import validate_image, validate_confidence

def get_image_obj_segments(img_file: UploadFile, confidence: float, predictor: ObjectSegmentator, csv_service: CSVService) -> Response:
    # Start counting the time
    start = time.time()

    # Validate the confidence threshold
    validate_confidence(confidence)
    
    # Validate the image file
    validate_image(img_file)

    # Read the image file into a stream
    img_stream = io.BytesIO(img_file.file.read())

    # Convert to a Pillow image
    img_obj = Image.open(img_stream)

    # Convert to a NumPy array
    img_array = np.array(img_obj)

    # Perform image segmentation using the provided predictor
    seg_img_pil, _ = predictor.segment_image(img_array, confidence)

    # Save the segmented image to a stream in JPEG format
    img_stream_masked = io.BytesIO()
    seg_img_pil.save(img_stream_masked, format="JPEG")
    img_stream_masked.seek(0)


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
    return Response(content=img_stream_masked.read(), media_type="image/jpeg")


def get_image_obj_segments_data(img_file: UploadFile, confidence: float, predictor: ObjectSegmentator, csv_service: CSVService) -> list[SegmentationInstanceData]:
    # Start counting the time
    start = time.time()

    # Validate the confidence threshold
    validate_confidence(confidence)

    # Validate the image file
    validate_image(img_file)

    # Read the image file into a stream
    img_stream = io.BytesIO(img_file.file.read())

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


def image_remove_items_from_list(img_file: UploadFile, confidence: float, items: list[str], predictor: ObjectSegmentator, csv_service: CSVService) -> Response:
    # Start counting the time
    start = time.time()

    # Validate the confidence threshold
    validate_confidence(confidence)

    # Validate the image file
    validate_image(img_file)


    # Read the image file into a stream
    img_stream = io.BytesIO(img_file.file.read())

    # Convert to a Pillow image
    img_obj = Image.open(img_stream)

    # Convert to a NumPy array
    img_array = np.array(img_obj)

    # Perform image segmentation using the provided predictor
    removed_img = predictor.remove_items_from_list(img_array, confidence, items)

    # Save the segmented image to a stream in JPEG format
    img_stream_masked = io.BytesIO()
    removed_img.save(img_stream_masked, format="JPEG")
    img_stream_masked.seek(0)

    # End counting the time
    end = time.time()

    # Register into CSV
    csv_service.write_csv(
        CSVItem(
            file_name=img_file.filename,
            image_size=human_size(len(img_stream.getbuffer())),
            prediction_type=ServiceType.IMAGE_REMOVE_ITEMS,
            datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            execution_time=end - start, 
            model=predictor.model_name,
            confidence_threshold=confidence
        )
    )

    # Return the segmented image as a FastAPI Response
    return Response(content=img_stream_masked.read(), media_type="image/jpeg")