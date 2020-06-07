import cv2
import os
import sys
import numpy as np
import uuid

from io_processing import *
from openvino.inference_engine import IENetwork, IECore

def create_output_image(image, output):
    '''
    With the bounding boxes generated from postprocessing,
    draw it on a copy of the input image and return the result
    '''
    output_image = image.copy()

    for i, box in enumerate(output):
        try:
            cv2.drawContours(output_image, [box], 0, (0, 255, 0), 2)
        except Exception as e:
            sys.exit(1)

    img_id = str(uuid.uuid4())
    return img_id, output_image

def perform_inference(bin_image):
    '''
    Performs inference on an input image with the given model
    '''

    path = resource_path("./openvino_model/text-detection-0004.xml")
    bin_path = path[:-3] + "bin"

    # Create inference engine and read network
    # from the IR provided by the pre-trained model(s)
    infer_engine = IECore()

    #Read and load the detection model
    try:
        infer_net = infer_engine.read_network(model=path, \
                                                weights=bin_path)
        exec_net =  infer_engine.load_network(network=infer_net, \
                                                 device_name="CPU")
    except Exception as e:
        print("Failed to read and load network of the detection model")
        print("Check again your model!")
        print(e)
        raise e

    # Get input layers from the network
    input_layer = next(iter(infer_net.inputs))

    # Retrieve the information about the model input from the shape
    n, c, h, w = infer_net.inputs[input_layer].shape

    # Read the input image and preprocess
    try:
        # image = cv2.imread(input_image)
        preprocessed_image = preprocess_for_detection(bin_image, h, w)
    except Exception as e:
        print("Failed detection preprocessing!")
        print("Check again your image name/path")
        raise e

    # Inference Request (Synchronous)
    exec_net.infer({input_layer: preprocessed_image})

    # Obtain the output of the inference request
    output = exec_net.requests[0].outputs # Pixel output
    detection_output = detect_text(output, bin_image.shape)

    # Convert from pixel -> boxes
    detected_boxes = generate_bounding_boxes(bin_image, detection_output)

    #Create output image with the list of bounding boxes and input image
    output_img_id, output_image = create_output_image(bin_image, detected_boxes)

    preprocessed_images = preprocess_for_recognition(bin_image, detected_boxes)

    img_data = recognize_text(preprocessed_images)

    # update_database(output_img_id, img_content)

    return output_img_id, output_image, img_data

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
