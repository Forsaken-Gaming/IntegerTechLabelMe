from PyQt5.QtCore import QObject, pyqtSignal
import os, shutil, time
import labelme.ryanVideoCreator.file_processor
from labelme.ryanVideoCreator.metrics_logging import Metrics

class VideoWorker(QObject):
    progress = pyqtSignal(int)
    stepText = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, imageList, lastOpenDir, frameFrom, frameTo, fps, onlyAnnotatedImages, collectMetrics, drawMidpoint):
        super().__init__()
        self.imageList = imageList
        self.lastOpenDir = lastOpenDir
        self.windowOpen = True
        self.frameFrom = max(frameFrom, 0)
        if (imageList):
            self.frameTo = min(frameTo, len(imageList))
        else:
            self.frameTo = 0
        self.fps = fps
        self.numberOfImages = self.frameTo - self.frameFrom
        self.currentImageIndex = 0
        self.onlyAnnotatedImages = onlyAnnotatedImages
        self.collectMetrics = collectMetrics
        self.drawMidpoint = drawMidpoint

    def run(self):
        # Get paths
        folderName = self.lastOpenDir.split("/")[-1]
        cachePath = os.path.join(os.path.expandvars(r"%TEMP%\LabelMeCache"), folderName) 
        outputPath = os.path.join(os.path.expanduser(r"~\Desktop"), folderName) 
        annotatedImagePath = os.path.join(outputPath, "Annotated_Images")
        videoPath = os.path.join(outputPath, "Video")

        if self.collectMetrics:
            print("Constructing metrics for " + folderName)
            metrics = Metrics(folderName)
            metrics.setDateAndTime()
        else: 
            print("Skipping metrics for " + folderName)
            metrics = None

        # Delete Annotated Image Cache if it is a repeat generation
        if (os.path.exists(annotatedImagePath)):
            shutil.rmtree(annotatedImagePath)
        
        # Create paths
        os.makedirs(cachePath, exist_ok=True)
        os.makedirs(outputPath, exist_ok=True)
        os.makedirs(annotatedImagePath, exist_ok=True)
        os.makedirs(videoPath, exist_ok=True)

        # Catch conditions in which the program should not run

        # Make sure a folder is loaded
        if not self.imageList:
            self.finished.emit()
            return
        # Make sure that your frame from isn't greater than the frame to
        if self.frameFrom > self.frameTo:
            self.finished.emit()
            return
        # Make sure there will be at least 1 frame in the video
        if self.numberOfImages <= 0:
            self.finished.emit()
            return
        # If the process was cancelled last time, make sure Ryan's scripts will run
        labelme.ryanVideoCreator.setInterrupted(False)
        
        # Cache images (passing in metrics to collect the number of frames)
        totalFrameCount = self.cacheImages(cachePath, metrics)

        # Annotate Images
        self.currentImageIndex = 0
        labelme.ryanVideoCreator.file_processor.save_annotated_images(cachePath, annotatedImagePath, self.annotatedImageSaved, self.frameFrom, self.frameTo, self.onlyAnnotatedImages, 100, metrics, self.drawMidpoint)

        # Add Images to Video
        self.currentImageIndex = 0
        labelme.ryanVideoCreator.video_maker.compile_frames_to_video(annotated_output_folder=annotatedImagePath, output_video_path=os.path.join(videoPath, "output.mp4"), callback=self.videoFrameAdded, video_fps=self.fps)
        
        # Print logged data to txt file
        if self.collectMetrics:
            metrics.setTotalFrameCount(totalFrameCount)
            metrics.logMetricsToFile()

        self.progress.emit(100)
        self.stepText.emit("Done! Video is in the folder on your Desktop")
        self.finished.emit()

    def annotatedImageSaved(self):
        self.currentImageIndex += 1
        percent = 50 + round(((self.currentImageIndex / self.numberOfImages) / 4) * 100)
        self.progress.emit(percent)
        self.stepText.emit(f"Annotating Images ({self.currentImageIndex} / {self.numberOfImages})")
    
    def videoFrameAdded(self):
        self.currentImageIndex += 1
        percent = 75 + round(((self.currentImageIndex / self.numberOfImages) / 4) * 100)
        self.progress.emit(percent)
        self.stepText.emit(f"Adding Frames To Video ({self.currentImageIndex} / {self.numberOfImages})")

    def cacheImages(self, cachePath, metrics):
        # Reset index
        self.currentImageIndex = 0
        for i in range(self.numberOfImages):
            # End the process if the window is suddenly closed
            if not self.windowOpen:
                return
            
            # Get the source and destination paths for the current png and json file
            sourceImagePath = self.imageList[i + self.frameFrom]
            imageNamewPath, ext = os.path.splitext(sourceImagePath)
            newImagePath = os.path.join(cachePath, imageNamewPath.split(os.sep)[-1])

            # Attempt to copy the image. Account for overload errors
            try:
                if not os.path.exists(newImagePath + ext):
                    shutil.copy(sourceImagePath, newImagePath + ext)
            except Exception:
                # try again after 10 seconds
                time.sleep(10)
                if not os.path.exists(newImagePath + ext):
                    shutil.copy(sourceImagePath, newImagePath + ext)

            # Attempt to copy the json. Account for overload errors
            try:
                if os.path.exists(imageNamewPath + ".json"):
                    shutil.copy(imageNamewPath + ".json", newImagePath + ".json")
            except Exception:
                # try again after 10 seconds
                time.sleep(10)
                if os.path.exists(imageNamewPath + ".json"):
                    shutil.copy(imageNamewPath + ".json", newImagePath + ".json")

            # Report back progress
            percent = round(((self.currentImageIndex / self.numberOfImages) / 2) * 100)
            self.progress.emit(percent)
            self.stepText.emit(f"Caching Images ({self.currentImageIndex} / {self.numberOfImages})")

            self.currentImageIndex += 1
        
        return self.currentImageIndex

    def windowClosed(self):
        self.windowOpen = False
        labelme.ryanVideoCreator.setInterrupted(True)
