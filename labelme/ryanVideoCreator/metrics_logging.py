import os
from datetime import datetime
from pathlib import Path

class Metrics:

    valid_labels = {
        "AID_TO_NAVIGATION_CHANNEL_MARKER", "AID_TO_NAVIGATION_GENERAL", "AID_TO_NAVIGATION_LARGE_BUOY", "AID_TO_NAVIGATION_LIGHTHOUSE",
        "AID_TO_NAVIGATION_SMALL_BUOY", "LARGE_GENERAL_OBSTACLE", "LARGE_VESSEL_CARGO", "LARGE_VESSEL_GENERAL","LARGE_VESSEL_MILITARY",
        "LARGE_VESSEL_OTHER", "LARGE_VESSEL_PASSENGER", "MEDIUM_VESSEL_FISHING", "MEDIUM_VESSEL_GENERAL",
        "MEDIUM_VESSEL_MILITARY", "MEDIUM_VESSEL_OTHER", "MEDIUM_VESSEL_TUG", "MEDIUM_VESSEL_TUG_IN_TOW", "MEDIUM_VESSEL_YACHT",
        "SAILBOAT", "SMALL_GENERAL_OBSTACLE", "SMALL_VESSEL_GENERAL", "SMALL_VESSEL_JET_SKI", "SMALL_VESSEL_MILITARY",
        "SMALL_VESSEL_OTHER", "SMALL_VESSEL_POWER_BOAT",
    }

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

    def compareChangeInLabelCount(self, curr_frame="Unannotated frame", curr_count=0, prev_count=0):
        '''
        curr_frame: name of the current frame (string)
        curr_count: number of labels in the current frame (int)
        prev_count: number of labels in the previous frame (int)
        '''
        if prev_count < curr_count:
            self.addMetric(curr_frame, "LABEL(S) APPEARED      " + str(curr_count - prev_count) + " label(s) entered")
        elif prev_count > curr_count:
            self.addMetric(curr_frame, "LABEL(S) DISAPPEARED   " + str(prev_count - curr_count) + " label(s) exited")
    
    def compareChangeInMidpoint(self, curr_frame, label_name, prev_avg_change, curr_avg_change, midpoint):
        '''
        Goal: find when a label experiences an abonormal drastic change
        '''
        avg_change_delta = abs(curr_avg_change - prev_avg_change) * 2
        print(str(curr_frame) + " stats - avg change delta, " + str(avg_change_delta) + ", midpoint: " + str(midpoint))
        if avg_change_delta > 0.10:
            self.addMetric(curr_frame, label_name + " at midpoint position [ " +  str(midpoint) + " ] had drastic movement (avg change delta between frames: [ " + str(avg_change_delta) + " ]")

    def flagUnannotated(self, curr_frame):
        '''
        Flags unnannoted frames
        '''
        self.addMetric(curr_frame, "UNANNOTATED FRAME")

    def flagInvalidLabel(self, curr_frame, label_name):
        '''
        Flags label names not found in valid_frames set
         - o(1) lookup, not using an array
        '''
        if label_name in self.valid_labels:
            return
        self.addMetric(curr_frame, f"INVALID LABEL          Improper name '{label_name}'")

    def addMetric(self, curr_frame, metric_str):
        '''
        Appends a string (which holds metrics of a partiular frame) to 'collective_frame_metrics'
        Args:
            curr_frame: frame name (string
            metric_str: metric information of a given frame, prepended to collective metrics output (string)
        '''
        self.collective_frame_metrics += curr_frame + ": " + metric_str + "\n"

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
                log_file.write("\nCollected Metrics:\n")
                if self.collective_frame_metrics != "":
                    log_file.write(self.collective_frame_metrics)
                else:
                    log_file.write("No anomalies or key metrics found in the data.\n")
                
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
        
    
        