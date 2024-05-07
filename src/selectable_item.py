from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QColor, QPainter
from PyQt5.QtCore import pyqtSignal, QObject, QRectF
from handle_item import HandleItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsPixmapItem
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


class ItemData(QObject):
    dataChanged = pyqtSignal()

class SelectableItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.handles = [HandleItem(self) for _ in range(4)]
        self.itemData = ItemData()
        self.hideHandles()

    def hideHandles(self):
        for handle in self.handles:
            handle.hide()

    def showHandles(self):
        for handle in self.handles:
            handle.show()

    def updateHandles(self):
        if not self.isSelected():
            self.hideHandles()
            return

        rect = self.boundingRect().adjusted(-10, -10, 10, 10)  # adjust for handle size
        positions = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]
        for handle, pos in zip(self.handles, positions):
            handle.setPos(pos)
            handle.show()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.isSelected():
            self.updateHandles()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.isSelected():
            self.itemData.dataChanged.emit()

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            pen = QPen(QColor('blue'), 3)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect())

    def boundingRect(self):
        # Must be implemented in the subclass to return the item's bounding rect
        return QRectF()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            if value:
                self.showHandles()
            else:
                self.hideHandles()
        return super().itemChange(change, value)



class SelectableVideoItem(SelectableItem, QGraphicsVideoItem):
    def __init__(self, url, parent=None):
        QGraphicsVideoItem.__init__(self, parent)
        SelectableItem.__init__(self, parent)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(url)))
        self.mediaPlayer.play()  # Start playing immediately; adjust as needed
        self.url = url

    def boundingRect(self):
        return self.nativeSize()  # Returns the video frame size

class SelectablePixmapItem(SelectableItem, QGraphicsPixmapItem):
    def __init__(self, pixmap=None, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)  # Initialize parent class
        SelectableItem.__init__(self, parent)       # Initialize SelectableItem
        if pixmap:
            self.setPixmap(pixmap)  # Set the pixmap after the base class initialization
    def boundingRect(self):
        if self.pixmap():
            return QRectF(self.pixmap().rect())
        return QRectF()