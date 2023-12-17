from PySide6 import QtWidgets, QtCore, QtGui
from ui.blankwidget import Ui_blankWidget


class BlankWidget(QtWidgets.QWidget):
    contrastUpdated = QtCore.Signal(float)
    sharpnessUpdated = QtCore.Signal(float)
    brightnessUpdated = QtCore.Signal(float)
    temperatureUpdated = QtCore.Signal(float)
    leftPressed = QtCore.Signal()
    rightPressed = QtCore.Signal()
    topPressed = QtCore.Signal()
    downPressed = QtCore.Signal()
    autoPosPressed = QtCore.Signal()

    def __init__(self, parent=None):
        super(BlankWidget, self).__init__(parent)

        self.ui = Ui_blankWidget()
        self.ui.setupUi(self)

        self.ui.contrastSlider.valueChanged.connect(self.contrastSliderChanged)
        self.ui.brightnessSlider.valueChanged.connect(
            self.brightnessSliderChanged)
        self.ui.sharpnessSlider.valueChanged.connect(
            self.sharpnessSliderChanged)
        self.ui.temperatureSlider.valueChanged.connect(
            self.temperatureSliderChanged)
        self.ui.contrastSpinBox.valueChanged.connect(
            self.contrastSpinBoxChanged)
        self.ui.brightnessSpinBox.valueChanged.connect(
            self.brightnessSpinBoxChanged)
        self.ui.sharpnessSpinBox.valueChanged.connect(
            self.sharpnessSpinBoxChanged)
        self.ui.temperatureSpinBox.valueChanged.connect(
            self.temperatureSpinBoxChanged)

        self.ui.blankLeftButton.clicked.connect(self.leftPressed.emit)
        self.ui.blankRightButton.clicked.connect(self.rightPressed.emit)
        self.ui.blankTopButton.clicked.connect(self.topPressed.emit)
        self.ui.blankDownButton.clicked.connect(self.downPressed.emit)
        self.ui.autoGridAlignmentButton.pressed.connect(
            self.autoPosPressed.emit)

    def contrastSliderChanged(self, value):
        value = value / 100.0
        self.ui.contrastSpinBox.setValue(value)
        self.contrastUpdated.emit(value)

    def brightnessSliderChanged(self, value):
        value = value / 100.0
        self.ui.brightnessSpinBox.setValue(value)
        self.brightnessUpdated.emit(value)

    def sharpnessSliderChanged(self, value):
        value = value / 100.0 * 2
        self.ui.sharpnessSpinBox.setValue(value)
        self.sharpnessUpdated.emit(value)

    def temperatureSliderChanged(self, value):
        value = value / 100.0
        self.ui.temperatureSpinBox.setValue(value)
        self.temperatureUpdated.emit(value)

    def contrastSpinBoxChanged(self, value):
        self.ui.contrastSlider.setValue(int(value * 100))
        self.contrastUpdated.emit(value)

    def brightnessSpinBoxChanged(self, value):
        self.ui.brightnessSlider.setValue(int(value * 100))
        self.brightnessUpdated.emit(value)

    def sharpnessSpinBoxChanged(self, value):
        self.ui.sharpnessSlider.setValue(int(value/2 * 100))
        self.sharpnessUpdated.emit(value)

    def temperatureSpinBoxChanged(self, value):
        self.ui.temperatureSlider.setValue(int(value * 100))
        self.temperatureUpdated.emit(value)

    def get_brightness(self):
        return self.ui.brightnessSpinBox.value()

    def get_contrast(self):
        return self.ui.contrastSpinBox.value()

    def get_sharpness(self):
        return self.ui.sharpnessSpinBox.value()

    def get_hue(self):
        return self.ui.temperatureSpinBox.value()

    def set_brightness(self, value):
        self.ui.brightnessSpinBox.setValue(value)

    def set_contrast(self, value):
        self.ui.contrastSpinBox.setValue(value)

    def set_sharpness(self, value):
        self.ui.sharpnessSpinBox.setValue(value)

    def set_hue(self, value):
        self.ui.temperatureSpinBox.setValue(value)
