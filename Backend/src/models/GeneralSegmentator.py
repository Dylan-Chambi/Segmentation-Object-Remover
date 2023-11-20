from abc import ABC


class GeneralSegmentator(ABC):
    def __init__(self, model):
        self.model = model

    def segment_image(self, image):
        pass