from PyQt5 import QtWidgets
from labelme.utils import VideoWorker
from PyQt5.QtCore import QThread


class CreateVideoDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(CreateVideoDialog, self).__init__(parent)
        self.parent = parent
        self.videoThread = None
        self.setWindowTitle("Annotated Video Creator")

        # overall layout
        layout = QtWidgets.QVBoxLayout()

        # progress bar
        progressBar = QtWidgets.QProgressBar()
        progressBar.setRange(0, 100)
        self.progressBar = progressBar


        # start button
        self.startButton = QtWidgets.QPushButton()
        self.startButton.setText("Generate Video from Current Folder")
        self.startButton.clicked.connect(self.createVideo)

        # stepLabel
        stepLabel = QtWidgets.QLabel()
        stepLabel.setText("Ready...")
        self.stepLabel = stepLabel

        # Frame range layout
        frameRangeLayout = QtWidgets.QHBoxLayout()
        specificRangeLayout = QtWidgets.QHBoxLayout()

        # Create Radio Buttons
        self.allFramesRadioButton = QtWidgets.QRadioButton("All Frames")
        self.specificFramesRadioButton = QtWidgets.QRadioButton("Specific Frames")
        self.allFramesRadioButton.clicked.connect(self.frameRangeButtonClicked)
        self.specificFramesRadioButton.clicked.connect(self.frameRangeButtonClicked)

        # Fame range button group
        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(self.allFramesRadioButton)
        self.buttonGroup.addButton(self.specificFramesRadioButton)


        # Specific range
        # From
        minVBox = QtWidgets.QVBoxLayout()
        minVBox.addWidget(QtWidgets.QLabel("From"))
        self.minFrameNumber = QtWidgets.QLineEdit()
        self.minFrameNumber.setText("0")
        minVBox.addWidget(self.minFrameNumber)

        # To
        maxVBox = QtWidgets.QVBoxLayout()
        maxVBox.addWidget(QtWidgets.QLabel("To"))
        self.maxFrameNumber = QtWidgets.QLineEdit()
        maxVBox.addWidget(self.maxFrameNumber)
        
        # If user is not in a folder, block the start button
        if self.parent.imageList:
            self.maxFrameNumber.setText(str(len(self.parent.imageList)))
        else:
            self.maxFrameNumber.setText("0")
            self.startButton.setDisabled(True)
        
        # Default to all frames
        self.allFramesRadioButton.click()

        # Set up specific frames layout
        specificRangeLayout.addWidget(self.specificFramesRadioButton)
        specificRangeLayout.addLayout(minVBox)
        specificRangeLayout.addLayout(maxVBox)

        # Complete Frame Range Layout
        frameRangeLayout.addWidget(self.allFramesRadioButton)
        frameRangeLayout.addLayout(specificRangeLayout)

        # FPS text
        fpsLayout = QtWidgets.QVBoxLayout()
        fpsLayout.addWidget(QtWidgets.QLabel("FPS"))
        self.fpsText = QtWidgets.QLineEdit()
        self.fpsText.setText("10")
        fpsLayout.addWidget(self.fpsText)

        # Annotated Images Checkbox
        self.onlyAnnotatedImages = QtWidgets.QCheckBox("Use Only Annotated Images")
        self.onlyAnnotatedImages.setToolTip("When checked, the video will contain only images that have a JSON beside them")
        self.onlyAnnotatedImages.click()

        fpsCheckCombo = QtWidgets.QHBoxLayout()
        fpsCheckCombo.addLayout(fpsLayout)
        fpsCheckCombo.addWidget(self.onlyAnnotatedImages)

        # Complete layout
        layout.addLayout(frameRangeLayout)
        layout.addLayout(fpsCheckCombo)
        layout.addWidget(self.startButton)
        layout.addWidget(progressBar)
        layout.addWidget(stepLabel)
        self.setLayout(layout)

    def frameRangeButtonClicked(self):
        if (self.allFramesRadioButton.isChecked()):
            self.minFrameNumber.setDisabled(True)
            self.maxFrameNumber.setDisabled(True)
        else:
            self.minFrameNumber.setDisabled(False)
            self.maxFrameNumber.setDisabled(False)

    def createVideo(self):
        self.progressBar.setValue(0)
        frameFrom = int(self.minFrameNumber.text())
        frameTo = int(self.maxFrameNumber.text())
        if self.allFramesRadioButton.isChecked():
            frameFrom = 0
            if (self.parent.imageList):
                frameTo = len(self.parent.imageList)
            else:
                frameTo = 0
        
        self.videoThread = QThread()
        self.worker = VideoWorker(self.parent.imageList, self.parent.lastOpenDir, frameFrom, frameTo, int(self.fpsText.text()), self.onlyAnnotatedImages.isChecked())
        self.worker.moveToThread(self.videoThread)

        self.videoThread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progressBar.setValue)
        self.worker.stepText.connect(self.stepLabel.setText)
        self.worker.finished.connect(self.videoThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.videoThread.finished.connect(self.videoThread.deleteLater)
        self.videoThread.finished.connect(self.resetButton)
        self.startButton.setDisabled(True)
        self.videoThread.start()
    
    def resetButton(self):
        self.startButton.setDisabled(False)

    def closeEvent(self, event):
        try:
            if self.videoThread and self.videoThread.isRunning():
                self.worker.windowClosed()
                self.videoThread.quit()
                self.videoThread.wait()
        except:
            event.accept()
            return
        event.accept()



            
            