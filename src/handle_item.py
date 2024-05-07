from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QGraphicsItem

class HandleItem(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(-10, -10, 20, 20, parent)
        self.setBrush(QColor('blue'))
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges)
        self.setZValue(100)
        self.setCursor(QCursor(Qt.SizeFDiagCursor))

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.adjustParent()

    def adjustParent(self):
        if not self.parentItem():
            return
        # Assuming symmetric handles and parent's transform origin is its center
        parentRect = self.parentItem().boundingRect()
        center = parentRect.center()
        self.parentItem().prepareGeometryChange()
        scaleFactor = ((self.scenePos() - center).manhattanLength() / (self.startPos - center).manhattanLength())
        self.parentItem().setScale(self.parentItem().scale() * scaleFactor)
        self.parentItem().updateHandles()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.startPos = self.scenePos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.parentItem().itemData.dataChanged.emit()