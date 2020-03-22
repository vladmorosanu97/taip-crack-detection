import os
import math
import cv2
import csv
from skimage.feature import local_binary_pattern
from scipy.stats import itemfreq
import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib
import cvutils

from LBP.AOP import Aspects


class TrainingModel(object):
    def __init__(self):
        self._train_images = None
        self._train_dict = None
        self._normalized_histograms = []
        self._image_paths = []
        self._class_labels = []

    @Aspects.param_validator
    def set_train_images(self, training_set_path):
        try:
            self._train_images = cvutils.imlist(training_set_path)
        except AssertionError as ae:
            print(ae)

    @property
    def train_images(self):
        return self._train_images

    # @Aspects.param_validator
    # @Aspects.file_checker
    def set_train_dict(self, image_labels_path):
        raw_train_dict = dict()
        if os.path.exists(image_labels_path) and Aspects.file_checker(image_labels_path):
            with open(image_labels_path, 'rt') as csvfile:
                try:
                    reader = csv.reader(csvfile, delimiter=' ')
                    for row in reader:
                        try:
                            raw_train_dict[row[0]] = int(row[1])
                        except IndexError:
                            pass
                except csv.Error as e:
                    print(e)
        else:
            print("No suitable file for image labels: {}".format(image_labels_path))

        self._train_dict = raw_train_dict

    @property
    def train_dict(self):
        return self._train_dict

    def set_raw_results(self):
        raw_histograms = []
        raw_img_paths = []
        raw_class_labels = []
        if self.train_images:
            for train_image in self.train_images:
                print("Done with {} for training".format(train_image))
                im = cv2.imread(train_image)
                im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # greyscale
                radius = 3
                no_points = 8 * radius  # 8 neighbours, 24 points
                lbp_mask = local_binary_pattern(im_gray, no_points, radius, method='uniform')
                x = itemfreq(lbp_mask.ravel())  # calculate the histogram
                lbp_hist = x[:, 1] / sum(x[:, 1])  # normalize
                raw_histograms.append(train_image)
                raw_img_paths.append(lbp_hist)
                raw_class_labels.append(self.train_dict[os.path.split(train_image)[1]])
        self._normalized_histograms = raw_histograms
        self._image_paths = raw_img_paths
        self._class_labels = raw_class_labels

    @property
    def normalized_histograms(self):
        return self._normalized_histograms

    @property
    def image_paths(self):
        return self._image_paths

    @property
    def class_labels(self):
        return self._class_labels

    @Aspects.param_validator
    @Aspects.exception_logger
    @Aspects.result_logger
    def serialize_raw_results(self, pickle_path):
        try:
            joblib.dump((self.normalized_histograms, self.image_paths, self.class_labels), pickle_path, compress=3)
            return pickle_path
        except(TypeError, KeyError):
            print("Something wrong")
            return 0

    @Aspects.exception_logger
    @Aspects.result_logger
    @Aspects.path_exists
    def display_results(self):
        nrows = math.ceil((len(self.train_images)) / 3)
        ncols = 3
        fig, axes = plt.subplots(nrows, ncols)
        for row in range(nrows):
            for col in range(ncols):
                try:
                    if Aspects.path_exists(self.image_paths[row * ncols + col]) and (row * ncols + col) < len(self.image_paths):
                        axes[row][col].imshow(cv2.imread(self.image_paths[row * ncols + col]))
                        axes[row][col].axis('off')
                        axes[row][col].set_title("{}".format(os.path.split(self.image_paths[row * ncols + col])[1]))
                except UnicodeDecodeError:
                    print(self.image_paths[row*ncols + col])
        fig.canvas.draw()
        im_ts = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        im_ts = im_ts.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        cv2.imshow("Training Set", im_ts)
        cv2.waitKey()
