import json
import math

import cv2
import os
from skimage.feature import local_binary_pattern
from scipy.stats import itemfreq
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib
import argparse as ap
import cvutils


def testing(testing_set_path, testing_set_labels):

    X_name, X_test, y_test = joblib.load("lbp_dataset.pkl")
    test_images = cvutils.imlist(testing_set_path)

    test_dic = {}
    with open(testing_set_labels, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            test_dic[row[0]] = int(row[1])

    results_all = {}

    for test_image in test_images:
        print("\nCalculating Normalized LBP Histogram for {}".format(test_image))
        im = cv2.imread(test_image)
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        radius = 3
        no_points = 8 * radius
        lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
        x = itemfreq(lbp.ravel())
        hist = x[:, 1]/sum(x[:, 1])
        results = []
        """
        Methods for comparing histograms:
            0: correlation
            1: chi-square
            2: intersection
            3/4: computes Bhattacharyya distance, which is related to Bhattacharyya coefficient
        Calculate the chi-squared distance and the sort the values(the lower the distance -> better result)
        """
        for index, x in enumerate(X_test):
            score = cv2.compareHist(np.array(x, dtype=np.float32), np.array(hist, dtype=np.float32), method=1)
            results.append((X_name[index], round(score, 3)))
        results = sorted(results, key=lambda score: score[1])
        results_all[test_image] = results
        print("Displaying scores for {} ** \n".format(test_image))
        for image, score in results:
            print("{} has score {}".format(image, score))

    return results_all


def display(results_all):

    for test_image, results in results_all.items():
        im = cv2.imread(test_image)
        nrows = math.ceil((len(results))/3)   # 2
        ncols = 3
        fig, axes = plt.subplots(nrows,ncols)
        fig.suptitle("** Scores for -> {}**".format(test_image))
        for row in range(nrows):
            for col in range(ncols):
                if row*ncols+col < len(results) and os.path.exists(results[row*ncols+col][0]):
                    axes[row][col].imshow(cv2.imread(results[row*ncols+col][0]))
                    axes[row][col].axis('off')
                    axes[row][col].set_title("Score {}".format(results[row*ncols+col][1]))
        fig.canvas.draw()
        im_ts = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        im_ts = im_ts.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        cv2.imshow("** Query Image -> {}**".format(test_image), im)
        cv2.imshow("** Scores for -> {}**".format(test_image), im_ts)
        cv2.waitKey()
        cv2.destroyAllWindows()


def record_results(results_all):

    with open("results", "wt", newline='') as csvfile:
        fieldnames = ["test_image_name", "compared_to", "score"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for key, values in results_all.items():
            for v in values:
                writer.writerow({
                    'test_image_name': os.path.basename(key),
                    'compared_to': os.path.basename(v[0]),
                    'score': v[1]
                })


