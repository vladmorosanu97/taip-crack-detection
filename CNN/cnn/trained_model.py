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

test_image = image.load_img(r"C:\Master\TAIP\cnn\random-image\Screenshot_3.png", target_size = (64,64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)

classifier = load_model("C:\Master\TAIP\cnn\models\my_model.h5")
result = classifier.predict(test_image)
print(result[0][0])

if result[0][0] >= 0.5:
    prediction = 'dog'
else:
    prediction = 'cat'
    
print(prediction)