import os
from datetime import datetime
from pathlib import Path

class Metrics:
    def __init__(self, folder_name, date=None, time=None):
        self.folder_name = folder_name
        self.label_count = 0
        self.total_frame_count = 0
        self.annotated_frame_count = 0
        self.date = date
        self.time = time
        self.desktop_dir = Path.home() / "Desktop"
        self.collective_frame_metrics = ""

    # Setter / mutator functions 

    def setFolderName(self, folder_name):
        '''
        Setter function to initialize folder name
        Args:
            string: folder name (where data is)
        '''
        self.folder_name = folder_name

    
    def setDateAndTime(self):
        '''
        Set date and time of when the metrics were collected
        '''
        current_datetime = datetime.now()
        self.date = current_datetime.date()
        self.time =  f"{current_datetime.hour}hr-{current_datetime.minute}min"

    def setTotalFrameCount(self, count):
        '''
        Set total frame count
        Args:
            integer: total num of frames
        '''
        self.total_frame_count = count

    # Computational getter functions

    def getAverageNumOfLabelsPerFrame(self):
        """
        Calculate the average number of labels per frame.
        Returns:
            float: Average number of labels per frame.
        """
        if self.total_frame_count == 0:
            return 0.0
        return round(self.label_count / self.total_frame_count, 2)

    
    # Increment functions to update counts

    def incrementLabelCount(self):
        self.label_count += 1

    def incrementLabelCount(self, additional):
        self.label_count += additional

    def incrementTotalFrameCount(self):
        self.total_frame_count += 1

    def incrementAnnotatedFrameCount(self):
        self.annotated_frame_count += 1

    def addMetric(self, frame_num, metric_str):
        '''
        Appends a string (which holds metrics of a partiular frame) to 'collective_frame_metrics'
        Args:
            integer: frame number
            string: metric information of a given frame
        '''
        self.collective_frame_metrics += "Frame " + frame_num + ": " + metric_str + "\n"

    def resetAllMetrics(self):
        """
        Reset all metrics and reset date and time.
        """
        self.label_count = 0
        self.total_frame_count = 0
        self.annotated_frame_count = 0
        self.collective_frame_metrics = ""
        self.setDateAndTime()

    def logMetricsToFile(self):
        """
        Log metrics to the logs folder and name after folder name
        """
        try:
            # Create the directory if it doesn't exist
            output_dir = os.path.join(self.desktop_dir, self.folder_name, "Metrics")
            os.makedirs(output_dir, exist_ok=True)

            # Create actual log file
            log_file_path = os.path.join(output_dir, f"{self.folder_name}_metrics_{self.date}_{self.time}.txt")
            with open(log_file_path, 'w') as log_file:
                # Intro data
                log_file.write(f"Metrics for folder '{self.folder_name}':\n")
                log_file.write(f"Date: {self.date}\n")
                log_file.write(f"Time: {self.time}\n")

                # Primary collected metrics
                log_file.write("\nCollected Metrics:")
                if self.collective_frame_metrics != "":
                    log_file.write(self.collective_frame_metrics)
                else:
                    log_file.write("\nNo anomalies or key metrics found in the data.\n")
                
                # Concluding metrics
                log_file.write("\nConcluding Metrics:\n")
                log_file.write(f"Number of Annotated Frames: {self.annotated_frame_count}\n")
                log_file.write(f"Number of Unannotated Frames: {self.total_frame_count - self.annotated_frame_count}\n")
                log_file.write(f"Total Number of Frames: {self.total_frame_count}\n")
                log_file.write(f"Total Number of Labels: {self.label_count}\n")
                log_file.write(f"Average Number of Labels per Frame: {self.getAverageNumOfLabelsPerFrame()}\n")
            print(f"Metrics logged to {log_file_path}")
        except Exception as e:
            print(e)
        
    
        