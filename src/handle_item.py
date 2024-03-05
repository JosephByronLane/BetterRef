from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor

class HandleItem(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(-5, -5, 10, 10, parent)  # Small circle with a radius of 5
        self.setBrush(QColor('blue'))
        self.parentItem = parent  # Reference to the SelectableImageItem
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(100)  # Ensure the handle is drawn above other items

    def mousePressEvent(self, event):
        self.startPos = self.scenePos()
        self.originPos = self.parentItem.pos()
        self.originSize = self.parentItem.boundingRect().size()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        currentPos = self.scenePos()
        delta = currentPos - self.startPos

        # Determine the scale factor while maintaining the aspect ratio
        scaleFactorX = (self.originSize.width() + delta.x()) / self.originSize.width()
        scaleFactorY = (self.originSize.height() + delta.y()) / self.originSize.height()
        scaleFactor = min(scaleFactorX, scaleFactorY)  # Maintain aspect ratio

        # Resize the parent item
        newWidth = max(self.originSize.width() * scaleFactor, 10)  # Minimum size limit
        newHeight = max(self.originSize.height() * scaleFactor, 10)  # Minimum size limit
        self.parentItem.prepareGeometryChange()
        self.parentItem.setPixmap(self.parentItem.pixmap().scaled(newWidth, newHeight, Qt.KeepAspectRatio))
        self.parentItem.updateHandles()  # Update handle positions

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)