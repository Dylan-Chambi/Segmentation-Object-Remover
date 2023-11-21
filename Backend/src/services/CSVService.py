import csv
import os
from functools import cache
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