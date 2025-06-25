import PIL.Image
import PIL.ImageEnhance
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage


class BrightnessContrastDialog(QtWidgets.QDialog):
    _base_value = 50

    def __init__(self, img, callback, parent=None):
        super(BrightnessContrastDialog, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Brightness/Contrast")

        sliders = {}
        layouts = {}
        layouts["KeepPreviousToggles"] = QtWidgets.QHBoxLayout()
        for title in ["Brightness:", "Contrast:"]:
            layout = QtWidgets.QHBoxLayout()
            title_label = QtWidgets.QLabel(self.tr(title))
            title_label.setFixedWidth(75)
            layout.addWidget(title_label)
            #
            slider = QtWidgets.QSlider(Qt.Horizontal)
            slider.setRange(0, 3 * self._base_value)
            slider.setValue(self._base_value)
            layout.addWidget(slider)
            #
            value_label = QtWidgets.QLabel(f"{slider.value() / self._base_value:.2f}")
            value_label.setAlignment(Qt.AlignRight)
            layout.addWidget(value_label)
            #
            slider.valueChanged.connect(self.onNewValue)
            slider.valueChanged.connect(
                lambda value, lbl=value_label: lbl.setText(f"{value / self._base_value:.2f}")
            )

            layouts[title] = layout
            sliders[title] = slider
        
        self.slider_brightness = sliders["Brightness:"]
        self.slider_contrast = sliders["Contrast:"]
        del sliders
        
        # Keep Previous Brightness Toggle
        self.keepPrevBrightnessToggle = QtWidgets.QCheckBox("Keep Previous Brightness")
        self.keepPrevBrightnessToggle.setChecked(self.parent._config["keep_prev_brightness"])
        self.keepPrevBrightnessToggle.clicked.connect(lambda: self.parent.enableKeepPrevBrightness(self.keepPrevBrightnessToggle.isChecked()))

        # Keep Previous Contrast Toggle
        self.keepPrevContrastToggle = QtWidgets.QCheckBox("Keep Previous Contrast")
        self.keepPrevContrastToggle.setChecked(self.parent._config["keep_prev_contrast"])
        self.keepPrevContrastToggle.clicked.connect(lambda: self.parent.enableKeepPrevContrast(self.keepPrevContrastToggle.isChecked()))

        layouts["KeepPreviousToggles"].addWidget(self.keepPrevBrightnessToggle)
        layouts["KeepPreviousToggles"].addWidget(self.keepPrevContrastToggle)
        

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(layouts["Brightness:"])
        layout.addLayout(layouts["Contrast:"])
        layout.addLayout(layouts["KeepPreviousToggles"])
        del layouts
        self.setLayout(layout)

        assert isinstance(img, PIL.Image.Image)
        self.img = img
        self.callback = callback

    def onNewValue(self, _):
        brightness = self.slider_brightness.value() / self._base_value
        contrast = self.slider_contrast.value() / self._base_value

        img = self.img
        if brightness != 1:
            img = PIL.ImageEnhance.Brightness(img).enhance(brightness)
        if contrast != 1:
            img = PIL.ImageEnhance.Contrast(img).enhance(contrast)

        qimage = QImage(
            img.tobytes(), img.width, img.height, img.width * 3, QImage.Format_RGB888
        )
        self.callback(qimage)
