from fastapi import File, UploadFile

def get_image_obj_segments(img_file: File, confidence: float):
    return {"message": "Hello World from image_seg.py"}