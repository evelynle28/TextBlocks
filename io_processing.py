import cv2
import numpy as np
import os
import pytesseract
import sqlite3
import uuid
import sys


from scipy.ndimage.measurements import label
from box_drawing import *
from PIL import Image


def detect_text(output, input_shape):
    '''
    Handle output of Text Detection model
    Extract the first blob - text/no-text classification
    Rescale to the original dimensions
    '''

    text_classification = output['model/segm_logits/add']

    text_output = np.empty([text_classification.shape[1],
                             input_shape[0],
                             input_shape[1]])


    # Resize outputs to the original
    for layer in range(len(text_classification[0])):
        text_output[layer] = cv2.resize(text_classification[0][layer],
                                        input_shape[0:2][::-1])

    return text_output

def preprocess_for_detection(input_image, height, width):
    '''
    Given an input image, height and width:
    - Resize the input image to the standard of the model
    - Transpose and reshape to fit the model's input requirement
    '''

    preprocessed_img = cv2.resize(np.copy(input_image), (width, height))

    # Put number of channel to first
    preprocessed_img = preprocessed_img.transpose((2,0,1))

    # Reshape and add the batch num to the first
    preprocessed_img = preprocessed_img.reshape(1, 3, height, width)

    return preprocessed_img

def generate_bounding_boxes(orginal_image, processed_output):
    '''
    Given the input image and its output from the text detection model:
        - Label text components in the input
        - Draw bounding boxes based on the labeled
    Return the list of boxes
    '''

    # Retrieve pixels that are classified as text
    # with confidence level > 0.5
    array = np.where(processed_output[1]>0.5, 1, 0)
    structure = np.ones((3, 3), dtype=np.int)

    labeled, ncomponents = label(array, structure)
    indices = np.indices(array.shape).transpose(1,2,0)

    boxes = get_boxes(labeled, ncomponents, indices, orginal_image)

    boxes = minimize_box_num(boxes)

    return boxes

def recognize_text(imgs_by_box):
    '''
    Handle the text recognition process
    Perform recognition on each of the preprocessed
    images and adjust the psm in order to optimize
    the result
    '''

    img_data = []
    for i, data in enumerate(imgs_by_box):
        box_coor = data[0]
        img = data[1]

        box_dict = {}

        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, np.array(img))


        text = pytesseract.image_to_string(Image.open(filename))

        modes = [6,7]

        invalid_chars = ['«', '¢', '—']
        if (len(text) == 0):
            for mode in modes:
                psm = '--psm ' + str(mode)
                text = pytesseract.image_to_string(Image.open(filename),\
                                                    lang='eng', config=psm)

                if any(x in text for x in invalid_chars):
                    continue
                if(len(text) != 0):
                    break

        box_dict['id'] = i
        box_dict['coors'] = box_coor
        box_dict['content'] = text


        os.remove(filename)
        img_data.append(box_dict)

    return img_data

def crop_image(center, h, w, org_img):
    '''
    Crop the part of the image bounded by the boxes generated
    during the text detection process
    '''
    ext_thres = 10
    tlX = center[0] - w/2
    tlY = center[1] - h/2
    brX = center[0] + w/2
    brY = center[1] + h/2
    new_crop = org_img.crop((tlX - ext_thres, tlY - ext_thres,\
                             brX + ext_thres, brY + ext_thres))

    return new_crop

def preprocess_for_recognition(img_cv, bounding_box_list):
    '''
    Preprocessing the image before applying pytesseract OCR
    '''
    img_gray = cv2.cvtColor(np.copy(img_cv), cv2.COLOR_BGR2GRAY )

    preprocessed_image = []

    for box in bounding_box_list:
        rect = cv2.minAreaRect(box)
        center, dims, angle = rect

        if (angle == -90):
            h, w = dims
        else:
            w, h = dims

        if abs(angle) % 90 != 0:
            rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
            result = cv2.warpAffine(img_gray, rot_mat,\
                                    img_gray.shape[:],\
                                    flags = cv2.INTER_LINEAR)

        img_pil = Image.fromarray(img_gray)

        img = crop_image(center, h, w, img_pil)

        preprocessed_box = [box.tolist(), img]
        preprocessed_image.append(preprocessed_box)

    return preprocessed_image











