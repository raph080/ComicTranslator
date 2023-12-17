from PySide6 import QtWidgets, QtCore, QtGui
import sys
import io
from PIL import Image, ImageQt
import imageprocessing
from graphicsscene import GraphicsScene


from ui.mainwindow import Ui_MainWindow

# requirements:
# 5*7 cells per frame


class Cell:
    def __init__(self, image: Image, origin: tuple = (0, 0)):
        self._origin = origin
        self._image = image
        self._blank_origin = (0, 0)
        self._mask = None
        self._contrast = None
        self._brightness = None
        self._sharpness = None
        self._hue = None

    def get_origin(self):
        return self._origin

    def set_origin(self, origin):
        self._origin = origin

    def get_blank_origin(self):
        return self._blank_origin

    def set_blank_origin(self, blank_origin):
        self._blank_origin = blank_origin

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image

    def get_mask(self):
        return self._mask

    def set_mask(self, mask):
        self._mask = mask

    def get_contrast(self):
        return self._contrast

    def set_contrast(self, contrast):
        self._contrast = contrast

    def get_brightness(self):
        return self._brightness

    def set_brightness(self, brightness):
        self._brightness = brightness

    def get_sharpness(self):
        return self._sharpness

    def set_sharpness(self, sharpness):
        self._sharpness = sharpness

    def get_hue(self):
        return self._hue

    def set_hue(self, hue):
        self._hue = hue


class TmpMask:
    def __init__(self, data, is_erase: bool = False):
        if isinstance(data, tuple):
            self._mask = imageprocessing.create_mask(data)
        else:
            self._mask = data

        self._is_erase = is_erase

    def get_mask(self):
        return self._mask

    def set_mask(self, mask):
        self._mask = mask

    def set_erase(self, state):
        self._is_erase = state

    def is_erase(self):
        return self._is_erase


def compose_masks(masks: list[TmpMask]) -> Image:
    mask = masks[0].get_mask()
    for tm in masks[1:]:
        if tm.is_erase():
            mask = imageprocessing.sub_images([mask, tm.get_mask()])
        else:
            mask = imageprocessing.add_images([mask, tm.get_mask()])
    return mask


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("My App")

        self._original_filepath = "/Users/raphaeljouretz/Documents/comic_translator/planche.tif"
        blank_filepath = "/Users/raphaeljouretz/Documents/comic_translator/blank.png"

        image = Image.open(self._original_filepath)

        cell_rectanlges = imageprocessing.get_cell_rectangles(image)
        self._cells: list[Cell] = []
        for rect in cell_rectanlges:
            x, y, w, h = rect
            cropped_image = imageprocessing.crop_image(image, (w, h), (-x, -y))
            cell = Cell(cropped_image, (x, y))
            self._cells.append(cell)

        self._cell_id = 0

        self.ui.actionPreviousCell.triggered.connect(self._prev_image)
        self.ui.actionNextCell.triggered.connect(self._next_image)
        self.ui.actionRemoveText.triggered.connect(self._add_letters_to_mask)
        self.ui.actionZoomOut.triggered.connect(self._zoom_out)
        self.ui.actionZoomIn.triggered.connect(self._zoom_in)
        self.ui.actionPaintMask.triggered.connect(self._edit_mask_clicked)
        self.ui.actionEraseMask.triggered.connect(self._edit_mask_clicked)
        self.ui.actionEditBlank.triggered.connect(self._edit_blank_clicked)
        self.ui.actionUndo.triggered.connect(self._undo)
        self.ui.actionRedo.triggered.connect(self._redo)
        self.ui.actionDiscard.triggered.connect(self._discard)
        self.ui.actionComposeLayers.triggered.connect(self._toggle_compsition)
        self.ui.actionAutoTextRemovalAndBlankAlignment.triggered.connect(
            self._set_auto_text_blank)
        self.ui.actionExportModification.triggered.connect(
            self._export_modifications)
        self.ui.actionExportComposition.triggered.connect(
            self._export_composition)

        group = QtGui.QActionGroup(self)
        group.addAction(self.ui.actionEraseMask)
        group.addAction(self.ui.actionPaintMask)
        group.addAction(self.ui.actionEditBlank)
        group.setExclusive(True)
        group.setExclusionPolicy(group.ExclusionPolicy.ExclusiveOptional)

        self._scene = GraphicsScene()
        self.ui.graphicsView.setScene(self._scene)

        self._scene.pressed.connect(self._mouse_pressed)
        self._scene.moved.connect(self._mouse_moved)
        self._scene.released.connect(self._mouse_released)

        self.ui.blankWidget.contrastUpdated.connect(self._refresh_draw_layer)
        self.ui.blankWidget.brightnessUpdated.connect(self._refresh_draw_layer)
        self.ui.blankWidget.sharpnessUpdated.connect(self._refresh_draw_layer)
        self.ui.blankWidget.temperatureUpdated.connect(
            self._refresh_draw_layer)

        self.ui.blankWidget.leftPressed.connect(
            lambda: self._move_blank(-1, 0))
        self.ui.blankWidget.rightPressed.connect(
            lambda: self._move_blank(1, 0))
        self.ui.blankWidget.topPressed.connect(
            lambda: self._move_blank(0, -1))
        self.ui.blankWidget.downPressed.connect(
            lambda: self._move_blank(0, 1))
        self.ui.blankWidget.autoPosPressed.connect(self._move_blank_auto)

        self.ui.paintWidget.letterRemovalPressed.connect(
            self._add_letters_to_mask)

        self._mouse_prev_pos = None
        self._is_mouse_pressed = False
        self._zoom_level = 1
        self._masks: list[TmpMask] = []
        self._text_mask: TmpMask = None
        self._redo_stack: list[TmpMask] = []
        self._original_blank = Image.open(blank_filepath)

        self._background_item = QtWidgets.QGraphicsPixmapItem()
        self._draw_layer_item = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._background_item)
        self._scene.addItem(self._draw_layer_item)

        self.ui.stackedWidget.hide()

        self._load_image(self._cell_id)

    def _get_cur_masks(self):
        masks = self._masks.copy()
        if self._text_mask:
            masks.insert(0, self._text_mask)
        return masks

    def _export_modifications(self):
        print("modification")

    def _export_composition(self):
        pixmap = QtGui.QPixmap(self._original_filepath)

        for cell in self._cells:
            mask = cell.get_mask()
            if mask:
                x, y = cell.get_origin()
                w = mask.width
                h = mask.height

                blank = self._generate_blank_for_cell(cell)
                imageprocessing.apply_mask_to_image(blank, mask)
                mask_pixmap = imageprocessing.pil_image_to_qpixmap(blank)
                # mask_pixmap = imageprocessing.pil_mask_to_pixmap(
                #     mask, color=(255, 0, 0, 0))

                painter = QtGui.QPainter(pixmap)

                target = QtCore.QRectF(x, y, w, h)
                source = QtCore.QRectF(0, 0, w, h)
                painter.drawPixmap(target, mask_pixmap, source)

                painter.end()
        pixmap.save("/Users/raphaeljouretz/Documents/comic_translator/out.png")

    def _is_auto_text_blank(self):
        return self.ui.actionAutoTextRemovalAndBlankAlignment.isChecked()

    def _set_auto_text_blank(self, state):
        if state:
            self._add_letters_to_mask()
            self._move_blank_auto()
        else:
            self._text_mask = None
            self._refresh_draw_layer()

    def _undo(self):
        if not len(self._masks):
            return

        self._redo_stack.append(self._masks.pop())
        self._refresh_draw_layer()

    def _redo(self):
        if not len(self._redo_stack):
            return

        self._masks.append(self._redo_stack.pop())
        self._refresh_draw_layer()

    def _toggle_compsition(self):
        self._refresh_draw_layer()

    def _edit_mask_clicked(self, state):
        if state:
            self.ui.paintWidget.set_letter_detection_group_visibility(
                self.ui.actionPaintMask.isChecked())
            self.ui.stackedWidget.show()
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.hide()

    def _edit_blank_clicked(self, state):
        if state:
            self.ui.stackedWidget.show()
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            self.ui.stackedWidget.hide()

    def _zoom_in(self):
        anim = QtCore.QTimeLine(150, self)
        anim.setUpdateInterval(30)
        view = self.ui.graphicsView

        def scalingTime(x):
            view.scale(1.1, 1.1)

        anim.valueChanged.connect(scalingTime)
        anim.start()

    def _zoom_out(self):
        anim = QtCore.QTimeLine(150, self)
        anim.setUpdateInterval(30)
        view = self.ui.graphicsView

        def scalingTime(x):
            view.scale(0.9, 0.9)

        anim.valueChanged.connect(scalingTime)
        anim.start()

    def _move_blank_auto(self):
        pattern = Image.open(
            '/Users/raphaeljouretz/Documents/comic_translator/match.tif')
        cell = self._get_cur_cell()
        image = cell.get_image()
        blank_origin = imageprocessing.find_pattern(image, pattern)
        self._get_cur_cell().set_blank_origin(blank_origin)

        self._refresh_draw_layer()

    def _move_blank(self, x, y):
        cell = self._get_cur_cell()
        blank_origin = cell.get_blank_origin()
        blank_origin = (blank_origin[0] + x, blank_origin[1] + y)
        cell.set_blank_origin(blank_origin)

        self._refresh_draw_layer()

    def _generate_blank_for_cell(self, cell: Cell) -> Image:
        image = cell.get_image()
        blank_origin = cell.get_blank_origin()
        blank = imageprocessing.crop_image(
            self._original_blank, image.size, blank_origin)

        blank_widget = self.ui.blankWidget
        brightness = blank_widget.get_brightness()
        contrast = blank_widget.get_contrast()
        sharpness = blank_widget.get_sharpness()
        hue = blank_widget.get_hue()

        blank = self._apply_effect_blank(
            blank,
            brightness=brightness,
            contrast=contrast,
            sharpness=sharpness,
            hue=hue)

        return blank

    def _apply_effect_blank(self, blank, brightness=None, contrast=None,
                            sharpness=None, hue=None) -> Image:
        if brightness != None:
            blank = imageprocessing.set_brightness(blank, brightness)
        if contrast != None:
            blank = imageprocessing.set_contrast(blank, contrast)
        if sharpness != None:
            blank = imageprocessing.set_sharpness(blank, sharpness)
        if hue != None:
            blank = imageprocessing.set_hue(blank, hue)
        return blank

    def _get_cur_cell(self) -> Cell:
        return self._cells[self._cell_id]

    def _mouse_pressed(self, pos: QtCore.QPoint):

        if (not self.ui.actionPaintMask.isChecked() and
                not self.ui.actionEraseMask.isChecked()):
            return

        self._is_mouse_pressed = True
        self._mouse_prev_pos = pos
        self._redo_stack = []

        cell = self._get_cur_cell()
        image = cell.get_image()
        self._masks.append(
            TmpMask(image.size, self.ui.actionEraseMask.isChecked()))

        self._mouse_moved(pos)

    def _mouse_moved(self, pos: QtCore.QPoint):
        if not self._is_mouse_pressed:
            return

        brush_color = "white"
        radius = self.ui.paintWidget.get_size()
        mask = self._masks[-1].get_mask()
        imageprocessing.draw_line(
            mask, radius, brush_color, self._mouse_prev_pos.toTuple(), pos.toTuple())

        self._mouse_prev_pos = pos

        self._refresh_draw_layer(still_drawing=True)

    def _mouse_released(self, pos: QtCore.QPoint):
        if not self._is_mouse_pressed:
            return

        self._is_mouse_pressed = False

        radius = self.ui.paintWidget.get_hardness()
        tmpMask = self._masks[-1]
        mask = tmpMask.get_mask()
        mask = imageprocessing.blur(mask, radius)
        tmpMask.set_mask(mask)

    def _add_letters_to_mask(self):
        image = self._get_cur_cell().get_image()
        border = self.ui.paintWidget.get_border()
        blur = self.ui.paintWidget.get_blur()
        text_mask = imageprocessing.get_text_mask(image, blur, border)
        self._text_mask = TmpMask(text_mask)

        self._refresh_draw_layer()

    def _refresh_draw_layer(self, still_drawing=False):
        cell = self._get_cur_cell()
        image = cell.get_image()

        tmp_masks = self._get_cur_masks()

        if not tmp_masks:
            size = image.size
            pixmap = QtGui.QPixmap(size[0], size[1])
            pixmap.fill(QtCore.Qt.transparent)
            self._draw_layer_item.setPixmap(pixmap)
            return

        if still_drawing:
            radius = self.ui.paintWidget.get_hardness()
            last_mask = tmp_masks[-1]
            tmp_mask = imageprocessing.blur(last_mask.get_mask(), radius)
            is_erase = last_mask.is_erase()
            tmp_masks = tmp_masks[:-1] + [TmpMask(tmp_mask, is_erase)]

        mask = compose_masks(tmp_masks)

        pixmap = None
        if self.ui.actionComposeLayers.isChecked():
            blank = self._generate_blank_for_cell(cell)
            imageprocessing.apply_mask_to_image(blank, mask)
            pixmap = imageprocessing.pil_image_to_qpixmap(blank)
        else:
            pixmap = imageprocessing.pil_mask_to_pixmap(
                mask, color=(255, 0, 0, 0))

        self._draw_layer_item.setPixmap(pixmap)

    def _refresh_background(self):
        cell = self._get_cur_cell()
        image = cell.get_image()

        pixmap = imageprocessing.pil_image_to_qpixmap(image)
        self._background_item.setPixmap(pixmap)

    def _prev_image(self):
        id = max(self._cell_id - 1, 0)
        self._save_cell_state()
        self._load_image(id)

    def _next_image(self):
        id = min(self._cell_id + 1, len(self._cells)-1)
        self._save_cell_state()
        self._load_image(id)

    def _load_image(self, id):
        self._cell_id = id
        cell = self._get_cur_cell()

        self._masks = []
        self._text_mask = None
        self._redo_stack = []

        if cell.get_mask():
            self._masks.append(TmpMask(cell.get_mask()))

        if cell.get_brightness():
            blank_widget = self.ui.blankWidget
            blank_widget.set_brightness(cell.get_brightness())
            blank_widget.set_contrast(cell.get_contrast())
            blank_widget.set_sharpness(cell.get_sharpness())
            blank_widget.set_hue(cell.get_hue())

        if self._is_auto_text_blank():
            self._set_auto_text_blank(state=True)

        self._refresh_background()
        self._refresh_draw_layer()

    def _save_cell_state(self):
        cell = self._get_cur_cell()

        masks = self._get_cur_masks()
        if masks:
            cell.set_mask(compose_masks(masks))

        blank_widget = self.ui.blankWidget
        brightness = blank_widget.get_brightness()
        contrast = blank_widget.get_contrast()
        sharpness = blank_widget.get_sharpness()
        hue = blank_widget.get_hue()

        cell.set_brightness(brightness)
        cell.set_contrast(contrast)
        cell.set_sharpness(sharpness)
        cell.set_hue(hue)

    def _discard(self):
        self._load_image(self._cell_id)
