# Program to detect vanishing points in single images
import os

import cv2
from Robust_may_13_tuning import HoughDetect_May_13
from Kalman_Filter import Matrix
import time
import numpy as np


def tri_crop(image, b_left, top, b_right):
    pts = np.array([b_left, top, b_right])
    cropped = image[0:151, 0:151].copy()
    pts = pts - pts.min(axis=0)
    mask = np.zeros(cropped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    bg = np.ones_like(cropped, np.uint8) * 255  # add white background
    cv2.bitwise_not(bg, bg, mask=mask)

    return cropped


filelist = os.listdir('IN')
for img_file in filelist[:]:
    if img_file.endswith(".jpg"):
        # Create a full screen window for viewing the results
        # cv2.namedWindow('Window', cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty('Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Read from Image

        print('STATS: ' + img_file)
        fname = 'IN/'+img_file
        img = cv2.imread(fname)
        print("Image size: {0}".format(img.shape[:2]))

        # Image Resolution
        res = 1

        # Initial state and covariance matrix
        x = Matrix([[960. * res], [330. * res]])  # 960, 330 are close to half of the original image height and width
        P = Matrix([[10000., 0.], [0., 10000.]])

        count_hough = 0
        t1 = []
        while count_hough < 1:
            t0 = time.time()
            img_result, x, P, measurement, crop_s, crop_f = HoughDetect_May_13(img, x, P, resolution=res)
            t1 = time.time() - t0
            count_hough += 1

        print('Vanishing Point coordinates = {0}'.format(x))
        print('Processing time = {0:.2f} sec'.format(t1) + '\n')

        file_result = 'OUT/' + os.path.splitext(os.path.basename(img_file))[0] + '_center' + '.jpg'
        cropped_file_result = 'OUT/' + os.path.splitext(os.path.basename(img_file))[0] + '_cropped' + '.jpg'
        tri_file_result = 'OUT/' + os.path.splitext(os.path.basename(img_file))[0] + '_triangle' + '.jpg'
        y1 = crop_s[1]
        height, width, channels = img.shape
        print(crop_s, crop_f, height, width)
        crop_img = img[y1:height, 0:width]
        cv2.imwrite(cropped_file_result, crop_img)
        cv2.imwrite(file_result, img_result)

        cv2.imwrite(tri_file_result, tri_crop(img, [0, 0], [150, 150], [0, 150]))
        # cv2.imshow('Window', img_result)
