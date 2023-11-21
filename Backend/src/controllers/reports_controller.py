from src.services.csv_service import CSVService
from fastapi.responses import StreamingResponse


def get_reports(csv_service: CSVService) -> StreamingResponse:
    return csv_service.get_csv_file()