from tensorflow.keras.models import load_model
from io import BytesIO
import base64
from IPython.display import display
from PIL import Image
import json

import numpy as np
from tensorflow.keras.preprocessing import image


class CnnPredictor():
    def __init__(self, model_path):
        self.classifier = load_model(model_path)


    def get(self, image_base64) -> list:
        test_image = image.load_img(BytesIO(base64.b64decode(image_base64)), target_size = (128,128), color_mode = "grayscale")
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = self.classifier.predict(test_image)
        result = result[0][0]
        return result