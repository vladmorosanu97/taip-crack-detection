# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 18:54:41 2019

@author: vladm
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense

classifier = Sequential()

classifier.add(Convolution2D(32, 3,3, input_shape = (64, 64, 3), activation = 'relu'))

classifier.add(MaxPooling2D(pool_size = (2,2)))

classifier.add(Flatten())

classifier.add(Dense(128, activation = 'relu'))
classifier.add(Dense(1, activation = 'sigmoid'))

classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


from tensorflow.keras.preprocessing.image import ImageDataGenerator


train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(
        r"C:\Master\TAIP\cnn\training-set\Convolutional_Neural_Networks\dataset\training_set",
        target_size = (64,64),
        batch_size = 32,
        class_mode = 'binary')

test_set = test_datagen.flow_from_directory(
        r"C:\Master\TAIP\cnn\training-set\Convolutional_Neural_Networks\dataset\test_set",
        target_size = (64,64),
        batch_size = 32,
        class_mode = 'binary')


from IPython.display import display
from PIL import Image

classifier.fit_generator(
        training_set, 
        steps_per_epoch = 10,
        epochs = 1,
        validation_data = test_set,
        validation_steps = 10)


import numpy as np
from tensorflow.keras.preprocessing import image

print(result[0][0])
if result[0][0] >= 0.5:
    prediction = 'crack'
else:
    prediction = 'non crack'

print(prediction)


#from tensorflow.keras.models import load_model

#classifier.save(r"C:\Master\TAIP\cnn\models\my_model-2.h5")

#new_model = load_model("C:\Master\TAIP\cnn\models\my_model-2.h5")

#result = new_model.predict(test_image)

#if result[0][0] >= 0.5:
#    prediction = 'dog'
#else:
#    prediction = 'cat'

#print(prediction)