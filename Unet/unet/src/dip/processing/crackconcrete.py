import dip.image as im
import cv2


# preprocesarea imaginii - returneaza 'masca'
def image_preprocessor(image):
    image = cv2.bitwise_not(image)
    image = im.gauss_filter(image, (3, 3))
    image = im.equalize_light(image)
    image = im.light(image, bright=-20, contrast=-20)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = im.threshold(image, min_limit=127)
    return image


def label_preprocessor(label):
    label = cv2.cvtColor(label, cv2.COLOR_BGR2GRAY)
    label = im.threshold(label, min_limit=127)
    return label
