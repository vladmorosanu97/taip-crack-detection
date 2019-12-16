# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 23:40:35 2019

@author: vladm
"""

from tensorflow.keras.models import load_model


from IPython.display import display
from PIL import Image


import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf
print(tf.version.VERSION)
test_image = image.load_img(r"C:\Master\TAIP\rotate-images\horizontal-dataset\horizontal-00001-135.jpg", target_size = (128,128), color_mode = "grayscale")
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)

classifier = load_model(r"C:\Master\TAIP\models\model2.h5")
result = classifier.predict(test_image)

print(result[0][0])
if result[0][0] >= 0.5:
    prediction = 'crack'
else:
    prediction = 'not crack'

print(prediction)
"""
Created on Mon Nov  4 22:00:06 2019

@author: vladm
"""

