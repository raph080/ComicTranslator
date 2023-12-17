from PySide6 import QtWidgets, QtCore, QtGui


class GraphicsScene(QtWidgets.QGraphicsScene):
    pressed = QtCore.Signal(QtCore.QPointF)
    released = QtCore.Signal(QtCore.QPointF)
    moved = QtCore.Signal(QtCore.QPointF)

    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

    def mouseMoveEvent(self, ev: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.moved.emit(ev.scenePos())

    def mousePressEvent(self, ev: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.pressed.emit(ev.scenePos())
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.released.emit(ev.scenePos())
        return super().mouseReleaseEvent(ev)
