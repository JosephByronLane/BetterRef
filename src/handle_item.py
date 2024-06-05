from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import QPointF, Qt, QLineF 
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt
class HandleItem(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(-20, -20, 40, 40, parent) 
        self.setBrush(QColor('blue'))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(100)   
        self.setCursor(QCursor(Qt.SizeFDiagCursor)) 

    def mousePressEvent(self, event):
        QGraphicsEllipseItem.mousePressEvent(self, event) 
        self.startPos = self.scenePos()
        self.startScale = self.parentItem().scale()
        self.originalSize = self.parentItem().boundingRect().size()

        # Disable movement of the parent item
        self.parentItem().setFlag(QGraphicsItem.ItemIsMovable, False)

    def mouseMoveEvent(self, event):
        QGraphicsEllipseItem.mouseMoveEvent(self, event)

        currentPos = self.mapToScene(event.pos())
        delta = currentPos - self.startPos

        center = self.parentItem().sceneBoundingRect().center()
        startVector = self.startPos - center
        currentVector = currentPos - center

        if startVector.manhattanLength() != 0:
            scaleFactor = currentVector.manhattanLength() / startVector.manhattanLength()
        else:
            scaleFactor = 1

        scaleFactor = 1 + (scaleFactor - 1) / 2

        self.parentItem().setTransformOriginPoint(self.parentItem().boundingRect().width() / 2, self.parentItem().boundingRect().height() / 2)
        self.parentItem().setScale(self.startScale * scaleFactor)

        self.parentItem().itemData.dataChanged.emit()

    def mouseReleaseEvent(self, event):
        QGraphicsEllipseItem.mouseReleaseEvent(self, event) 

        # Re-enable movement of the parent item
        self.parentItem().setFlag(QGraphicsItem.ItemIsMovable, True)

        if hasattr(self.parentItem(), 'updateGroupHandles'):
            self.parentItem().updateGroupHandles()
        else:
            self.parentItem().updateHandles()