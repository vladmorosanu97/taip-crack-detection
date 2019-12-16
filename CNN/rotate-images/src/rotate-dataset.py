# -*- coding: utf-8 -*-

from rotate_images import RotateImage
"""
Created on Sun Dec 15 19:06:01 2019

@author: vladm
"""
from os import listdir
from os.path import isfile, join

vertical_dataset_path = r"C:\Master\TAIP\rotate-images\vertical-dataset"
horizontal_dataset_path = r"C:\Master\TAIP\rotate-images\horizontal-dataset"
vertical_horizontal_path = r"C:\Master\TAIP\rotate-images\vertical-horizontal-dataset"

directory = r"C:\Master\TAIP\training-datasets\concrete-crack-images-for-classification\Concrete Crack Images for Classification\Positive"
onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
for file in onlyfiles:
    abs_path = join(directory, file)
    print(abs_path)
    ri = RotateImage(vertical_dataset_path, horizontal_dataset_path, vertical_horizontal_path)
    ri.perform_rotates(abs_path)