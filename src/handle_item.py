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
        self.startPos = self.scenePos()
        self.originPos = self.parentItem.pos()
        self.originScale = self.parentItem.scale()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        currentPos = self.scenePos()
        delta = currentPos - self.startPos

        if delta.manhattanLength() == 0:
            return

        originalDiagonal = (self.originPos - self.parentItem.mapToScene(self.parentItem.boundingRect().bottomRight())).manhattanLength()
        newDiagonal = (self.originPos - currentPos).manhattanLength()
        scaleFactor = newDiagonal / originalDiagonal

        self.parentItem.setScale(self.originScale * scaleFactor)

        self.parentItem.itemData.dataChanged.emit()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
