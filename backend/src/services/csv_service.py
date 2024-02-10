import csv
import os
import time

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from src.config.config import get_settings

SETTINGS = get_settings()

class CSVItem():
    def __init__(self, file_name, image_size, prediction_type, datetime, execution_time, model, confidence_threshold):
        self.file_name = file_name
        self.image_size = image_size
        self.prediction_type = prediction_type
        self.datetime = datetime
        self.execution_time = execution_time
        self.model = model
        self.confidence_threshold = confidence_threshold

    def to_list(self):
        return [self.file_name, self.image_size, self.prediction_type, self.datetime, self.execution_time, self.model, self.confidence_threshold]


class CSVService():
    def __init__(self):
        self.csv_path = SETTINGS.csv_path
        self.csv_headers = ["file_name", "image_size", "prediction_type", "datetime", "execution_time", "model", "confidence_threshold"]

        # create csv file if not exists
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "a") as f:
                f.write(",".join(self.csv_headers) + "\n")
        

    def write_csv(self, data: CSVItem):
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data.to_list())

    def read_csv(self) -> list:
        with open(self.csv_path, "r") as f:
            reader = csv.reader(f)
            data = list(reader)
        return data
    
    def get_csv_file(self) -> StreamingResponse:
        if not os.path.exists(self.csv_path):
            raise HTTPException(status_code=404, detail="CSV file not found")
        
        with open(self.csv_path, mode="r", encoding="utf-8") as file:
            csv_data = file.read()

        response = StreamingResponse(iter([csv_data]), media_type="text/csv")

        response.headers["Content-Disposition"] = f'attachment; filename="report-{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.csv"'
        
        return response