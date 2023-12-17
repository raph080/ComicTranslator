from PySide6 import QtWidgets, QtCore, QtGui
from ui.paintwidget import Ui_paintWidget
import imageprocessing
from PIL import Image


class PaintWidget(QtWidgets.QWidget):
    sizeUpdated = QtCore.Signal(float)
    hardnessUpdated = QtCore.Signal(float)
    borderUpdated = QtCore.Signal(float)
    blurUpdated = QtCore.Signal(float)
    letterRemovalPressed = QtCore.Signal()

    def __init__(self, parent=None):
        super(PaintWidget, self).__init__(parent)

        self.ui = Ui_paintWidget()
        self.ui.setupUi(self)

        self.ui.sizeSlider.valueChanged.connect(
            self.size_slider_changed)
        self.ui.hardnessSlider.valueChanged.connect(
            self.hardness_slider_changed)
        self.ui.borderSlider.valueChanged.connect(
            self.border_slider_changed)
        self.ui.blurSlider.valueChanged.connect(
            self.blur_slider_changed)

        self.ui.sizeSpinBox.valueChanged.connect(
            self.size_spinbox_changed)
        self.ui.hardnessSpinBox.valueChanged.connect(
            self.hardness_spinbox_changed)
        self.ui.borderSpinBox.valueChanged.connect(
            self.border_spinbox_changed)
        self.ui.blurSpinBox.valueChanged.connect(
            self.blur_spinbox_changed)

        self.ui.letterRemovalButton.clicked.connect(
            self.letterRemovalPressed.emit)

        self._update_brush_preview()

    def size_slider_changed(self, value):
        self.ui.sizeSpinBox.setValue(value)
        self.sizeUpdated.emit(value)
        self._update_brush_preview()

    def hardness_slider_changed(self, value):
        self.ui.hardnessSpinBox.setValue(value)
        self.hardnessUpdated.emit(value)
        self._update_brush_preview()

    def border_slider_changed(self, value):
        self.ui.borderSpinBox.setValue(value)
        self.borderUpdated.emit(value)

    def blur_slider_changed(self, value):
        self.ui.blurSpinBox.setValue(value)
        self.blurUpdated.emit(value)

    def size_spinbox_changed(self, value):
        self.ui.sizeSlider.setValue(value)
        self.sizeUpdated.emit(value)
        self._update_brush_preview()

    def hardness_spinbox_changed(self, value):
        self.ui.hardnessSlider.setValue(value)
        self.hardnessUpdated.emit(value)
        self._update_brush_preview()

    def border_spinbox_changed(self, value):
        self.ui.borderSlider.setValue(value)
        self.borderUpdated.emit(value)

    def blur_spinbox_changed(self, value):
        self.ui.blurSlider.setValue(value)
        self.blurUpdated.emit(value)

    def get_hardness(self):
        return self.ui.hardnessSpinBox.value()

    def get_size(self):
        return self.ui.sizeSpinBox.value()

    def get_border(self):
        return self.ui.borderSpinBox.value()

    def get_blur(self):
        return self.ui.blurSpinBox.value()

    def _update_brush_preview(self):
        size = self.ui.previewLabel.size().toTuple()
        preview = Image.new(
            mode="RGBA", size=size, color=(255, 0, 0, 0))

        radius1 = self.get_size()
        imageprocessing.draw_disc(
            preview, (size[0]/2, size[1] / 2), "red", radius1)

        radius2 = radius1 * self.get_hardness() / 100
        preview = imageprocessing.blur(preview, radius2)

        pixmap = imageprocessing.pil_image_to_qpixmap(preview)
        self.ui.previewLabel.setPixmap(pixmap)

    def set_letter_detection_group_visibility(self, state):
        self.ui.letterDetectionGroup.setHidden(not state)
