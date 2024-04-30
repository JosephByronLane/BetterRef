from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPen

class HandleItem(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(-10, -10, 20, 20, parent)
        self.setBrush(QColor('blue'))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(100)
        self.parentItem = parent

    def mousePressEvent(self, event):
        self.startPos = self.mapToScene(event.pos())
        self.originPos = self.parentItem.pos()
        self.originSize = self.parentItem.pixmap().size()
        self.startScale = self.parentItem.scale()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        currentPos = self.mapToScene(event.pos())
        delta = (currentPos - self.startPos) * self.startScale  # Apply current scale to delta

        # Calculate diagonal scaling factor
        startDiag = (self.originSize.width() ** 2 + self.originSize.height() ** 2) ** 0.5
        newDiag = startDiag + delta.manhattanLength()
        scaleFactor = newDiag / startDiag

        self.parentItem.setScale(self.startScale * scaleFactor)
        self.parentItem.itemData.dataChanged.emit()  # Emit signal to update any external data
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)