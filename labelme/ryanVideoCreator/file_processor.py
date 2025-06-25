

import os
import cv2
import json
import base64
import numpy as np
from labelme.ryanVideoCreator.drawing import draw_annotations_on_image
from labelme.ryanVideoCreator.metrics_logging import Metrics

global interrupted
interrupted = False

def decode_image_data(image_data):
    """
    can't work on pngs directly- need to convert using cv2.imdecode #TODO why? 

    """
    img_data = base64.b64decode(image_data)
    np_array = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

def process_annotation_file(json_path, subfolder_path, annotated_output_folder, onlyAnnotatedImages, text_position_offset=100, metrics=None):
    """

    This function reads the annotation data from a JSON file, retrieves the image path
    or data, and saves an annotated version of the image.

    Args:
        json_path: The path to the JSON file containing annotations.
        subfolder_path : The folder containing the associated image files.
        annotated_output_folder : The folder to save the annotated image.
        text_position_offset: Offset for positioning the filename text.
        metrics: Keeping track of the number of frames that are annotated vs unannotated

    Why this approach:
        - Separating this function allows handling one file at a time, making it easier
          to debug and test.

    """
    # Try to pull the image path from the json
    try:
        with open(json_path + ".json", 'r') as f:
            annotation_data = json.load(f)
        image_filename = annotation_data.get('imagePath')
        if metrics != None:
            metrics.incrementAnnotatedFrameCount()
    except:
        # If unable to find the json, assume the image file name from the name of the json
        # if told to do so by user
        annotation_data = None
        image_filename = json_path.split(os.sep)[-1] + ".png"

        if metrics != None:
            metrics.flagUnannotated(image_filename)
    
        if (onlyAnnotatedImages):
            return (0, image_filename)

    image_path = os.path.join(subfolder_path, image_filename)
    if not os.path.exists(image_path):
        print(f"Warning: Image file '{image_filename}' does not exist. Skipping file.")
        return (0, image_filename + "(warning, file not found)")

    image = cv2.imread(image_path) 
    #or decode_image_data(annotation_data.get('imageData'))
    (annotated_image, label_count) = draw_annotations_on_image(image, annotation_data, image_filename, text_position_offset, metrics)
    output_image_path = os.path.join(annotated_output_folder, image_filename)
    cv2.imwrite(output_image_path, annotated_image)
    if metrics != None:
        metrics.incrementLabelCount(label_count)
    
    return (label_count, image_filename)

def save_annotated_images(subfolder_path, annotated_output_folder, callback, indexFrom, indexTo, onlyAnnotatedImages, text_position_offset=100, metrics=None):
    """
    Processes all annotation files in a folder and saves annotated images.

    """
    # Get all of the PNG files in the directory
    png_files = sorted([
        f for f in os.listdir(subfolder_path)
        if f.lower().endswith('.png')
    ])
    # Annotate each frame
    prev_label_count = 0
    for i in range(indexTo - indexFrom):
        # Check if the window was closed
        if (interrupted):
            return
        # Get the json path of
        image_path = os.path.join(subfolder_path, os.path.splitext(png_files[indexFrom + i])[0])
        try:
            curr_label_count, image_file_name = process_annotation_file(image_path, subfolder_path, annotated_output_folder, onlyAnnotatedImages, text_position_offset, metrics)

            # Compare num of labels in curr vs prev frame (if collecting metrics)
            if metrics != None:
                metrics.compareChangeInLabelCount(image_file_name, curr_label_count, prev_label_count)
                prev_label_count = curr_label_count
        except Exception as e:
            print(f"Error processing file {image_path}: {e}")
        callback()

def setInterrupted(newVal):
    global interrupted
    interrupted = newVal