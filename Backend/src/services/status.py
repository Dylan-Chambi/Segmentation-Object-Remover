from src.models.ObjectSegmentator import ObjectSegmentator
from src.schemas.Status import Status
from src.schemas.StatusEndpoints import StatusEndpoints
from src.config.config import get_settings
from src.utils.data_info import MODEL_DESCRIPTION, SERVICE_ENDPOINTS

SETTINGS = get_settings()



def get_service_status(predictor_model: ObjectSegmentator) -> Status:
    model_data_info = predictor_model.model_info()
    response: Status = Status(
        yolo_version=SETTINGS.yolo_version,
        description=MODEL_DESCRIPTION,
        num_layers=model_data_info[0],
        num_parameters=model_data_info[1],
        gflops=model_data_info[3],
        endpoints=SERVICE_ENDPOINTS
    )
    return response