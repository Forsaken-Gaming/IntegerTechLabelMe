
import os
import cv2
from natsort import natsorted
import labelme.ryanVideoCreator

def compile_frames_to_video(annotated_output_folder, output_video_path, callback, video_fps=10.0,  video_codec='mp4v'):
    """
    Combines image frames into a video.

    This function reads all image files in the specified folder, sorts them in order,
    and compiles them into a video using the specified frame rate and codec.

    Args:
        annotated_output_folder (str): The folder containing annotated image files.
        output_video_path (str): The path where the output video will be saved.
        callback (function): A callback function to be called after each frame is added.
        video_fps (float, optional): Frames per second for the video. Default is 10.0.
        video_codec (str, optional): Codec to use for the video. Default is 'mp4v'.
        metrics (object, optional): An object to collect metrics, if enabled.
    """
    png_files = natsorted([f for f in os.listdir(annotated_output_folder) if f.endswith(".png")])
    if not png_files:
        return
    first_image_path = os.path.join(annotated_output_folder, png_files[0])
    frame = cv2.imread(first_image_path)
    height, width, _ = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*video_codec)
    video = cv2.VideoWriter(output_video_path, fourcc, video_fps, (width, height))

    for image_file in png_files:
        # if metrics is not None:
        #     metrics.incrementTotalFrameCount()

        if (labelme.ryanVideoCreator.interrupted):
            return
        img_path = os.path.join(annotated_output_folder, image_file)
        frame = cv2.imread(img_path)
        video.write(frame)
        callback()

    video.release()