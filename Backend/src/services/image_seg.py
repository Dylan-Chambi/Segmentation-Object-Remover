from fastapi import File, UploadFile, HTTPException, status, Response, Depends
from src.models.ObjectSegmentator import ObjectSegmentator
from src.models.SegmentationData import SegmentationInstanceData
import io
from PIL import Image
import numpy as np

def get_image_obj_segments(img_file: UploadFile, confidence: float, predictor: ObjectSegmentator):
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

    # Return the segmented image as a FastAPI Response
    return Response(content=img_stream.read(), media_type="image/jpeg")


def get_image_obj_segments_data(img_file: UploadFile, confidence: float, predictor: ObjectSegmentator) -> list[SegmentationInstanceData]:
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

    # Return the segmented image data
    return seg_data
