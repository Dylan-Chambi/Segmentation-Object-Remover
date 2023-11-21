from enum import Enum

class ServiceType(str, Enum):
    IMAGE_SEGMENTATION = "IMAGE_SEGMENTATION"
    IMAGE_DATA_SEG = "IMAGE_DATA_SEG"