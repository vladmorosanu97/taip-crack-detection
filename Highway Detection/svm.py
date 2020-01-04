import matplotlib
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import display

import pandas as pd
import numpy as np

from PIL import Image

from skimage.feature import hog
from skimage.color import rgb2grey

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC

from sklearn.metrics import roc_curve, auc

import aspectlib

OUTPUT_FOLDER = 'D:\Faculta - MOC I\TAIP\Lab4\Output'
IMG_PATH = 'highway.jpg'
BLOCK_NORM = 'L2-Hys'


def remove_png_files_from_path(path):
    for r, d, f in os.walk(path):
        for file in f:
            if '.png' in file:
                print('Remove on file ', file)


def image_to_array(file_path):
    img = Image.open(file_path)
    return np.array(img)


class SVM(object):
    def create_features(self, img, block_norm):
        if block_norm is None:
            return
        # flatten three channel color image
        color_features = img.flatten()
        # convert image to greyscale
        grey_image = rgb2grey(img)
        # get HOG features from greyscale image
        hog_features, hog_image = hog(grey_image, visualize=True, block_norm=block_norm, pixels_per_cell=(16, 16))

        plt.imshow(hog_image, cmap=mpl.pyplot.gray())
        plt.show()

        # combine color and hog features into a single array
        flat_features = np.hstack((color_features, hog_features))
        return flat_features

    def path_exists(path):
        return os.path.exists(path)

    def path_is_file(path):
        return os.path.isfile(path)

    def path_is_image(path):
        return path.lower().endswith(('.png', '.jpg', '.jpeg'))


model = SVM()

img_array = image_to_array(IMG_PATH)
print(img_array.shape)
new_img = img_array[350:450, 0:100, :]

Image.fromarray(new_img, mode='RGB').save('temp.jpg')

plt.imshow(img_array)
plt.imshow(new_img)
plt.show()

img_features = model.create_features(new_img, BLOCK_NORM)

exit()


def aop_svm():
    @aspectlib.Aspect
    def create_features(*args):
        print("********** Create a feature aspect **********")
        remove_png_files_from_path(OUTPUT_FOLDER)

        yield aspectlib.Proceed

    @aspectlib.Aspect
    def create_features_mop(*args):
        print("********** Create a mop features aspect **********")
        if args[1] is None:
            img_features = model.create_features(new_img, BLOCK_NORM)

        yield aspectlib.Proceed

    with aspectlib.weave(SVM.create_features, create_features, subclasses=False):
        model = SVM()

        img_array = image_to_array(IMG_PATH)
        print(img_array.shape)
        new_img = img_array[350:450, 0:100, :]

        Image.fromarray(new_img, mode='RGB').save('temp.jpg')

        plt.imshow(img_array)
        plt.imshow(new_img)
        plt.show()

        img_features = model.create_features(new_img, None)

    with aspectlib.weave(SVM.create_features, create_features_mop, subclasses=False):
        model = SVM()

        img_array = image_to_array(IMG_PATH)
        print(img_array.shape)
        new_img = img_array[350:450, 0:100, :]

        Image.fromarray(new_img, mode='RGB').save('temp.jpg')

        plt.imshow(img_array)
        plt.imshow(new_img)
        plt.show()

        img_features = model.create_features(new_img)

# aop_svm()