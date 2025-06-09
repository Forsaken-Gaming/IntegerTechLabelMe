

import os
import cv2
import json
import base64
import numpy as np
from labelme.ryanVideoCreator.drawing import draw_annotations_on_image

global interrupted
interrupted = False

def decode_image_data(image_data):
    """
    can't work on pngs directly- need to convert using cv2.imdecode #TODO why? 

    """
    img_data = base64.b64decode(image_data)
    np_array = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

def process_annotation_file(json_path, subfolder_path, annotated_output_folder, text_position_offset=100):
    """

    This function reads the annotation data from a JSON file, retrieves the image path
    or data, and saves an annotated version of the image.

    Args:
        json_path: The path to the JSON file containing annotations.
        subfolder_path : The folder containing the associated image files.
        annotated_output_folder : The folder to save the annotated image.
        text_position_offset: Offset for positioning the filename text.

    Why this approach:
        - Separating this function allows handling one file at a time, making it easier
          to debug and test.

    """
    with open(json_path, 'r') as f:
        annotation_data = json.load(f)

    image_filename = annotation_data.get('imagePath')
    if not image_filename:
        print(f"Warning: No 'imagePath' found in {json_path}. Skipping file.")
        return

    image_path = os.path.join(subfolder_path, image_filename)
    if not os.path.exists(image_path):
        print(f"Warning: Image file '{image_filename}' does not exist. Skipping file.")
        return

    image = cv2.imread(image_path) 
    #or decode_image_data(annotation_data.get('imageData'))
    annotated_image = draw_annotations_on_image(image, annotation_data, image_filename, text_position_offset)
    output_image_path = os.path.join(annotated_output_folder, image_filename)
    cv2.imwrite(output_image_path, annotated_image)

def save_annotated_images(subfolder_path, annotated_output_folder, callback, indexFrom, indexTo, text_position_offset=100):
    """
    Processes all annotation files in a folder and saves annotated images.

    """
    dir = os.listdir(subfolder_path)
    png_files = sorted([
        f for f in os.listdir(subfolder_path)
        if f.lower().endswith('.png')
    ])
    for i in range(indexTo - indexFrom):
        if (interrupted):
            return
        json_path = os.path.join(subfolder_path, os.path.splitext(png_files[indexFrom + i])[0] + ".json")
        try:
            process_annotation_file(json_path, subfolder_path, annotated_output_folder, text_position_offset)
        except Exception as e:
            print(f"Error processing file {json_path}: {e}")
        callback()

def setInterrupted(newVal):
    global interrupted
    interrupted = newVal