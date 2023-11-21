from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
from .generaL_segmentation import GeneralSegmentator
from .segmentation_inst_data import SegmentationInstanceData
from src.utils.constants import MASK_ALPHA
from src.config.config import get_settings

SETTINGS = get_settings()

class ObjectSegmentator(GeneralSegmentator):
    def __init__(self):
        self.model_name = SETTINGS.yolo_version
        self.model = YOLO('./Backend/src/tf_models/' + SETTINGS.yolo_version)
        self.transparency = MASK_ALPHA
        super().__init__(self.model)


    def model_info(self):
        return self.model.info()

    def convert_to_transparency(self, image: Image, background_color: tuple, transparency: int = 0) -> Image:
        # Convert the image to RGBA format
        image = image.convert("RGBA")

        # Get pixel data
        pixel_data = image.getdata()

        # Create a new list of pixels with adjusted transparency
        new_pixels = [
            (0, 0, 0, 0) if item[:3] == (0, 0, 0) else (background_color[0], background_color[1], background_color[2], transparency)
            for item in pixel_data
        ]

        # Create a new image with adjusted pixels
        new_image = Image.new("RGBA", image.size)
        new_image.putdata(new_pixels)

        return new_image
    
    def get_class_colors(self, class_ids: list[str]) -> dict[str, tuple[int, int, int]]:
        class_colors = {}
        for class_id in class_ids:
            if class_id not in class_colors:
                class_colors[class_id] = tuple(random.randint(0, 255) for _ in range(3))
        return class_colors
    
    def draw_class_text(self, draw: ImageDraw, polygon: list[tuple[int, int]], class_id: str):
        # Convert floating points to integers
        polygon_int = [(int(p[0]), int(p[1])) for p in polygon]

        # Calculate position for text
        text_position = (
            polygon_int[0][0] + (polygon_int[1][0] - polygon_int[0][0]) // 2,
            polygon_int[0][1] + (polygon_int[2][1] - polygon_int[0][1]) // 2
        )

        # Draw class text
        draw.text(text_position, class_id, fill=(255, 255, 255, 255), font=ImageFont.truetype("arial.ttf", 30))

    def dilate_background_image(self, bg_img: Image) -> Image:
        bg_img_array = np.array(bg_img)
        kernel = np.ones((5,5),np.uint8)
        bg_img_dilated = cv2.dilate(bg_img_array, kernel, iterations=2)
        return Image.fromarray(bg_img_dilated, 'RGB')
    
    def invert_and_transparency(self, img):
        img_inverted = ImageOps.invert(img)
        return self.convert_to_transparency(img_inverted, tuple(random.randint(0, 255) for _ in range(3)), self.transparency)

    def segment_image(self, image: np.ndarray, confidence: float):
        # Read results
        results = self.model.predict(image, conf=confidence)

        class_ids = []
        scores = []
        masks = []
        polygons = []
        images_mask_bin = []
        images_mask = []

        for result in results:
            boxes = result.boxes.cpu().numpy()

            for class_id in boxes.cls:
                class_ids.append(result.names[int(class_id)])

            for conf in boxes.conf:
                scores.append(conf)

            if result.masks is not None and len(result.masks) > 0:
                for mask in result.masks:
                    masks.append(mask.data[0].numpy())
                    polygons.append(mask.xy[0])

        # Create a PIL image from the original image
        image_pil = Image.fromarray(np.array(image), 'RGB')

        # Scale masks to the size of the original image
        height, width = image_pil.size

        # Define a dictionary to store class colors
        class_colors = self.get_class_colors(class_ids)

        bg_img = np.zeros((width, height, 3), dtype=np.uint8)
        bg_img = Image.fromarray(bg_img, 'RGB')

        # Iterate over masks, polygons, and class_ids simultaneously
        for mask, polygon, class_id in zip(masks, polygons, class_ids):
            predicted_img = np.zeros((width, height, 3), dtype=np.uint8)
            predicted_img = Image.fromarray(predicted_img, 'RGB')

            # Get the color corresponding to the class or generate a random one if it's new
            class_color = class_colors[class_id]

            mask_binary = np.array(mask * 255, dtype=np.uint8)
            mask_img = Image.fromarray(mask_binary, 'L').resize((height, width))

            predicted_img.paste(mask_img, (0, 0), mask_img)

            images_mask_bin.append(mask_img)

            bg_img.paste(mask_img, (0, 0), mask_img)

            # Convert the image and save the result
            image_result = self.convert_to_transparency(predicted_img, class_color, self.transparency)

            draw = ImageDraw.Draw(image_result)

            self.draw_class_text(draw, polygon, class_id)

            images_mask.append(image_result)

        # Dilate the background image
        bg_img = self.dilate_background_image(bg_img)

        # Invert the colors of the background image
        bg_img = self.invert_and_transparency(bg_img)
        images_mask.append(bg_img)

        # Place the images on the original image
        image_pil.convert("RGBA")

        for image in images_mask:
            image_pil.paste(image, (0, 0), image)

        segmentation_instances = []

        for class_id, score, polygon in zip(class_ids, scores, polygons):
            inst = SegmentationInstanceData(class_name=str(class_id), seg_mask_polygon=np.array(polygon).tolist(), score=float(score))
            segmentation_instances.append(inst)

        return image_pil, segmentation_instances
    