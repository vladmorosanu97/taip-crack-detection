import os
import pickle

import pandas as pd
import numpy as np

from PIL import Image

from skimage.feature import hog
from skimage.color import rgb2grey
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

DATASET_DIR_POS = 'D:\\Faculta - MOC I\\TAIP\\Lab4\\selected\\highway'
DATASET_DIR_NEG = 'D:\\Faculta - MOC I\\TAIP\\Lab4\\selected\\no_highway'
OUTPUT_DIR = 'D:\\Faculta - MOC I\\TAIP\\Lab4\\Output'
SAVE_MODEL_NAME = 'saved_model_wihout_pca.pkl'

HOG_BLOCK_NORM = 'L2-Hys'
SVM_PXS_PER_CELL = (16, 16)
NO_IMAGES = 300
PCA_NO_COMPONENTS = NO_IMAGES

TEST_SIZE = .3
SPLIT_RANDOM_STATE = 1234123
SVC_RANDOM_STATE = 42


def image_to_array(file_path):
    img = Image.open(file_path)
    return np.array(img)


def create_features(img_array):
    # flatten three channel color image
    color_features = img_array.flatten()
    # convert image to greyscale
    grey_image = rgb2grey(img_array)
    # get HOG features from greyscale image
    hog_features = hog(grey_image, visualize=False, block_norm=HOG_BLOCK_NORM, pixels_per_cell=SVM_PXS_PER_CELL)

    # combine color and hog features into a single array
    flat_features = np.hstack((color_features, hog_features))

    return flat_features


def create_feature_matrix(dir_path):
    features_list = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            img_path = os.path.join(root, file)

            img_array = image_to_array(img_path)
            image_features = create_features(img_array)

            features_list.append(image_features)

    # convert list of arrays into a matrix
    feature_matrix = np.array(features_list)
    return feature_matrix


def pca_reducing_features(feature_matrix):
    # define standard scaler
    ss = StandardScaler()
    # run this on our feature matrix
    feature_standard = ss.fit_transform(feature_matrix.reshape(1, -1))

    pca = PCA(n_components=PCA_NO_COMPONENTS)
    # use fit_transform to run PCA on our standardized matrix
    feature_pca = pca.fit_transform(feature_standard)

    return feature_pca


def train_and_save_model(save_model_name):
    highway_matrix = create_feature_matrix(DATASET_DIR_POS)
    no_highway_matrix = create_feature_matrix(DATASET_DIR_NEG)

    full_feature_matrix = np.concatenate((highway_matrix, no_highway_matrix), axis=0)
    train_labels = [1.0] * NO_IMAGES + [0.0] * NO_IMAGES

    # train_set_pca = pca_reducing_features(full_feature_matrix)
    #
    # print(train_set_pca.shape)

    x = pd.DataFrame(full_feature_matrix)
    y = pd.Series(train_labels)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=TEST_SIZE, random_state=SPLIT_RANDOM_STATE)

    # define support vector classifier
    svm = SVC(kernel='linear', probability=True, random_state=SVC_RANDOM_STATE)

    # fit model
    svm.fit(x_train, y_train)

    # generate predictions
    y_pred = svm.predict(x_test)

    # calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print('Model accuracy is: ', accuracy)

    # save the classifier
    with open(save_model_name, 'wb') as fid:
        pickle.dump(svm, fid)


def load_and_predict(model_path, img_path):
    # load model again
    with open(model_path, 'rb') as fid:
        svm = pickle.load(fid)

    img_path = img_path

    img_features = [create_features(image_to_array(img_path))]

    prediction = svm.predict(img_features)

    if prediction == [1.]:
        return True
    else:
        return False


# train_and_save_model(SAVE_MODEL_NAME)

new_img_path = 'D:\\Faculta - MOC I\\TAIP\\Lab4\\selected\\highway\\22202_1.jpg'
print(load_and_predict(SAVE_MODEL_NAME, new_img_path))
