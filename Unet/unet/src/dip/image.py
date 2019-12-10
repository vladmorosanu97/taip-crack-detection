import setting.constant as const
import numpy as np
import cv2


def overlay(image, layer):
    if len(layer.shape) == 2:
        layer = cv2.cvtColor(layer, cv2.COLOR_GRAY2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    layer = cv2.cvtColor(layer, cv2.COLOR_BGR2BGRA)
    layer[np.where((layer == [0, 0, 0, 255]).all(axis=2))] = const.BACKGROUND_COLOR + [255]
    layer[np.where((layer == [255, 255, 255, 255]).all(axis=2))] = const.SEGMENTATION_COLOR + [255]
    layer = cv2.addWeighted(image, 0.6, layer, 0.4, 0)
    return layer


def light(image, bright, contrast):
    bright = bright * 1.2
    contrast = contrast * 2
    image = image * ((contrast / 127) + 1) - contrast + bright
    image = np.clip(image, 0, 255)
    return np.uint8(image)


def threshold(image, min_limit=None, max_limit=255, clip=0):
    if min_limit is None:
        min_limit = int(np.mean(image) + clip)
    _, image = cv2.threshold(image, min_limit, max_limit, cv2.THRESH_BINARY)
    return np.uint8(image)


def gauss_filter(image, kernel=(3, 3), iterations=1):
    for _ in range(iterations):
        image = cv2.GaussianBlur(image, kernel, 0)
    return np.uint8(image)


def equalize_light(image, limit=3, grid=(7, 7), gray=False):
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        gray = True
    clahe = cv2.createCLAHE(clipLimit=limit, tileGridSize=grid)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    if gray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return np.uint8(image)

