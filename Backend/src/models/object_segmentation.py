from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
from src.schemas.image_rem_items import Item
from .generaL_segmentation import GeneralSegmentator
from .segmentation_inst_data import SegmentationInstanceData
from src.utils.constants import MASK_ALPHA
from src.config.config import get_settings

SETTINGS = get_settings()

class ObjectSegmentator(GeneralSegmentator):
    def __init__(self):
        self.model_name = SETTINGS.yolo_version
        self.model = YOLO('./Backend/src/segmentation_models/' + SETTINGS.yolo_version)
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
            polygon_int[0][0] + (polygon_int[1][0] - polygon_int[0][0]) // 2 - 5,
            polygon_int[0][1] + (polygon_int[2][1] - polygon_int[0][1]) // 2
        )

        # Draw class text
        draw.text(text_position, class_id, fill=(255, 0, 0, 255), font=ImageFont.truetype("arial.ttf", 15))
    
    def invert_and_transparency(self, img):
        img_inverted = ImageOps.invert(img)
        return self.convert_to_transparency(img_inverted, tuple(random.randint(0, 255) for _ in range(3)), self.transparency)

    def segment_image(self, image: np.ndarray, confidence: float):
        # Read results
        results = self.model.predict(image, conf=confidence)

        class_ids = []
        instance_ids = []
        scores = []
        masks = []
        polygons = []
        images_mask_bin = []
        images_mask = []

        for result in results:
            boxes = result.boxes.cpu().numpy()

            for class_id in boxes.cls:
                class_ids.append(result.names[int(class_id)])
                class_count = class_ids.count(result.names[int(class_id)])
                instance_ids.append(class_count)

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

        # Invert the colors of the background image
        bg_img = self.invert_and_transparency(bg_img)

        # Add background image to the list of images
        class_ids.append("background")
        instance_ids.append(1)
        scores.append(1)
        polygons.append([(0, 0), (0, width), (height, width), (height, 0)])
        images_mask.append(bg_img)
        images_mask_bin.append(bg_img)
        
        # Place the images on the original image
        image_pil.convert("RGBA")

        for image in images_mask:
            image_pil.paste(image, (0, 0), image)

        segmentation_instances = []

        for class_id, instance_id, score, polygon in zip(class_ids, instance_ids, scores, polygons):
            inst = SegmentationInstanceData(class_name=str(class_id), instance_id=instance_id, seg_mask_polygon=np.array(polygon).tolist(), score=float(score))
            segmentation_instances.append(inst)

        return image_pil, segmentation_instances
    
    def remove_items_from_list(self, image: np.ndarray, confidence: float, item_list: list[Item]):
        # Read results
        results = self.model.predict(image, conf=confidence)

        class_ids = []
        instance_ids = []
        scores = []
        masks = []

        for result in results:
            boxes = result.boxes.cpu().numpy()

            for class_id in boxes.cls:
                class_ids.append(result.names[int(class_id)])
                class_count = class_ids.count(result.names[int(class_id)])
                instance_ids.append(class_count)

            for conf in boxes.conf:
                scores.append(conf)

            if result.masks is not None and len(result.masks) > 0:
                for mask in result.masks:
                    masks.append(mask.data[0].numpy())

        # Create a PIL image from the original image
        image_pil = Image.fromarray(np.array(image), 'RGB')

        # Scale masks to the size of the original image
        height, width = image_pil.size

        # Create a black background image
        bg_img = np.zeros((width, height, 3), dtype=np.uint8)
        bg_img = Image.fromarray(bg_img, 'RGB')

        # Iterate over masks, class_ids, and instance_ids simultaneously
        for mask, class_id, instance_id in zip(masks, class_ids, instance_ids):
            current_item = Item(class_name=class_id, instance_id=instance_id)
            if current_item in item_list:
                # Convert mask to PIL image
                to_delete_mask = np.array(mask * 255, dtype=np.uint8)
                to_delete_mask_img = Image.fromarray(to_delete_mask, 'L').resize((height, width))

                # Paste the original image over the black background using the inverted mask
                image_pil.paste(bg_img, (0, 0), to_delete_mask_img)
        
        bg_img = np.zeros((width, height, 3), dtype=np.uint8)
        bg_img = Image.fromarray(bg_img, 'RGB')

        # Iterate over masks, polygons, and class_ids simultaneously
        for mask, class_id in zip(masks, class_ids):
            predicted_img = np.zeros((width, height, 3), dtype=np.uint8)
            predicted_img = Image.fromarray(predicted_img, 'RGB')


            mask_binary = np.array(mask * 255, dtype=np.uint8)
            mask_img = Image.fromarray(mask_binary, 'L').resize((height, width))

            predicted_img.paste(mask_img, (0, 0), mask_img)


            bg_img.paste(mask_img, (0, 0), mask_img)

        # Invert the colors of the background image
        bg_img = ImageOps.invert(bg_img)
        bg_img = self.convert_to_transparency(bg_img, (0, 0, 0), 255)

        if "background" in [item.class_name for item in item_list]:
            # Remove the background mask from image
            image_pil.paste(bg_img, (0, 0), bg_img)

        return image_pil