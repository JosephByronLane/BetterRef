import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsPixmapItem
from PyQt5.QtGui import QColor, QPainter, QPixmap, QDragEnterEvent, QDropEvent, QPen
from PyQt5.QtCore import Qt, QMimeData
from selectable_item import SelectableImageItem

class InfiniteCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setSceneRect(-100000000, -100000000, 200000000, 200000000)

        self.setBackgroundBrush(QColor("#202020"))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setRenderHint(QPainter.Antialiasing, False)
        self.setWindowTitle("BetterRef")
        self.selectedItem = None

        self.is_middle_button_dragging = False
        self.last_drag_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.drag_position = event.globalPos()
        if event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and event.modifiers() == Qt.AltModifier):
            self.is_middle_button_dragging = True
            self.last_drag_position = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        else:
            item = self.itemAt(event.pos())
            if item and isinstance(item, SelectableImageItem):
                if self.selectedItem:
                    self.selectedItem.setSelected(False)
                item.setSelected(True)
                self.selectedItem = item
            else:
                if self.selectedItem:
                    self.selectedItem.setSelected(False)
                    self.selectedItem = None
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            delta = event.globalPos() - self.drag_position
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_position = event.globalPos()
        if self.is_middle_button_dragging:
            delta = event.pos() - self.last_drag_position
            self.last_drag_position = event.pos()

            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and event.modifiers() == Qt.AltModifier):
            self.is_middle_button_dragging = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier:
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        event.accept()
        sys.exit(0)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) > 0:
                image_path = urls[0].toLocalFile()

                view_position = event.pos()

                scene_position = self.mapToScene(view_position)

                self.addImageToScene(image_path, scene_position)

    def addImageToScene(self, image_path, position):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            item = SelectableImageItem(pixmap)
            
            image_center_x = position.x() - pixmap.width() / 2
            image_center_y = position.y() - pixmap.height() / 2

            item.setPos(image_center_x, image_center_y)
            self.scene.addItem(item)

    def wheelEvent(self, event):
        zoomInFactor = 1.25 
        zoomOutFactor = 1 / zoomInFactor

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        if event.angleDelta().y() > 0:
            self.scale(zoomInFactor, zoomInFactor)
        else:
            self.scale(zoomOutFactor, zoomOutFactor)

