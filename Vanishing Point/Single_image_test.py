# Program to detect vanishing points in single images
import os
import cv2
from Robust_may_13_tuning import HoughDetect_May_13
from Kalman_Filter import matrix
import time
import numpy as np


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


        # Image Resolution
        res = 1

        # Initial state and covariance matrix
        x = matrix([[960. * res], [330. * res]])  # 960, 330 are close to half of the original image height and width
        P = matrix([[10000., 0.], [0., 10000.]])

        count_hough = 0
        t1 = []
        while count_hough < 1:
            t0 = time.time()
            img_result, x, P, measurement = HoughDetect_May_13(img, x, P, resolution=res)
            t1 = time.time() - t0
            count_hough += 1

        print('Vanishing Point coordinates = {0}'.format(x))
        print('Processing time = {0:.2f} sec'.format(t1) + '\n')


        fileresult = 'OUT/' + os.path.splitext(os.path.basename(img_file))[0] + '_center' + '.jpg'
        cv2.imwrite(fileresult, img_result)

        #cv2.imshow('Window', img_result)