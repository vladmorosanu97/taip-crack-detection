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

test_image = image.load_img(r"C:\Master\TAIP\test-datasets\cracks\random-images\Screenshot_22.png", target_size = (64,64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)

classifier = load_model(r"C:\Master\TAIP\test-datasets\cracks\models\models.h5")
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

