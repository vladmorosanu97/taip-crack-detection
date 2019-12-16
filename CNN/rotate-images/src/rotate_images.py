from image_transformer import ImageTransformer
from util import save_image
import sys
import os
import numpy as np

#     Change main function with ideal arguments
#     then
#     python demo.py [name of the image] [degree to rotate] ([ideal width] [ideal height])
#     e.g.,
#     python demo.py images/000001.jpg 360
#     python demo.py images/000001.jpg 45 500 700
#
# Parameters:
#     img_path  : the path of image that you want rotated
#     shape     : the ideal shape of input image, None for original size.
#     theta     : the rotation around the x axis
#     phi       : the rotation around the y axis
#     gamma     : the rotation around the z axis (basically a 2D rotation)
#     dx        : translation along the x axis
#     dy        : translation along the y axis
#     dz        : translation along the z axis (distance to the image)
#
# Output:
#     image     : the rotated image


# Input image path

class RotateImage:
    
    def __init__(self, vertical_path, horizontal_path, vertica_horzontal_path):
        self.vertical_export_path = vertical_path
        self.horizontal_export_path = horizontal_path
        self.vertical_horizontal_export_path = vertica_horzontal_path
    
    def perform_rotates(self, image_path):
        self.rotate_vertical(image_path, self.vertical_export_path, 135, 255)
        self.rotate_horizontal(image_path, self.horizontal_export_path, 135, 255)
        self.rotate_horizontal_vertical(image_path, self.vertical_horizontal_export_path, 135, 255)
        
    def center_crop(self, img, new_width=128, new_height=128):
        width = img.shape[1]
        height = img.shape[0]
    
        if new_width is None:
            new_width = min(width, height)
    
        if new_height is None:
            new_height = min(width, height)
    
        left = int(np.ceil((width - new_width) / 2))
        right = width - int(np.floor((width - new_width) / 2))
    
        top = int(np.ceil((height - new_height) / 2))
        bottom = height - int(np.floor((height - new_height) / 2))
    
        if len(img.shape) == 2:
            center_cropped_img = img[top:bottom, left:right]
        else:
            center_cropped_img = img[top:bottom, left:right, ...]
        return center_cropped_img
    
    
    def rotate_vertical(self, path, export_path, rot_range_start, rot_range_end):
        image_shape = None
        it = ImageTransformer(path, image_shape)
        for ang in range(135, 225, 20):
            rotated_img = it.rotate_along_axis(theta = ang)
            rotated_img = self.center_crop(rotated_img, 128, 128)
            self.save_image(path, export_path, rotated_img, "vertical", ang)
    
    def rotate_horizontal(self, path, export_path, rot_range_start, rot_range_end):
        image_shape = None
        it = ImageTransformer(path, image_shape)
        for ang in range(135, 225, 20):
            rotated_img = it.rotate_along_axis(phi = ang)
            rotated_img = self.center_crop(rotated_img, 128, 128)
            self.save_image(path, export_path, rotated_img, "horizontal", ang)
            

    def rotate_horizontal_vertical(self, path, export_path, rot_range_start, rot_range_end):
        image_shape = None
        it = ImageTransformer(path, image_shape)
        for ang in range(150, 210, 15):
            rotated_img = it.rotate_along_axis(phi = ang, gamma = ang)
            rotated_img = self.center_crop(rotated_img, 128, 128)
            self.save_image(path, export_path, rotated_img, "vertical-horizontal", ang)
            
        
    def save_image(self, path, export_path, rotated_image, prefix, ang):
        name = os.path.basename(path).split(".")[0]
        save_image(export_path + "\\" + prefix + "-" + name + "-{}.jpg".format(str(ang).zfill(3)), rotated_image)
