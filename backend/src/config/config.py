from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="Backend/.env")
    
    api_name: str = "Image Background Remover API"
    revision: str = "local"
    yolo_version: str = "yolov8m-seg.pt" # El modelo a cargar debe estar en Backend/src/tf_models/
    log_level: str = "DEBUG"
    csv_path: str = "../utils/data.csv"

@cache
def get_settings() -> Settings:
    return Settings()