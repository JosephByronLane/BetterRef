from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import QPointF, Qt, QLineF  # Import QLineF for distance calculations
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

    def mouseMoveEvent(self, event):
        QGraphicsEllipseItem.mouseMoveEvent(self, event)  

        currentPos = self.mapToScene(event.pos())
        delta = currentPos - self.startPos

        # Calculate the center of the image
        center = self.parentItem().sceneBoundingRect().center()

        # Calculate the distance from the center to the start position and current position
        startDistance = (self.startPos - center).manhattanLength()
        currentDistance = (currentPos - center).manhattanLength()

        # Calculate the scale factor based on the change in distance
        if startDistance != 0:
            scaleFactor = currentDistance / startDistance
        else:
            scaleFactor = 1

        # Set the transform origin point to the center of the image
        self.parentItem().setTransformOriginPoint(center)

        # Scale the image by the calculated scale factor
        self.parentItem().setScale(self.startScale * scaleFactor)

        self.parentItem().itemData.dataChanged.emit()

    def mouseReleaseEvent(self, event):
        self.parentItem().updateHandles() 
        super().mouseReleaseEvent(event)

    def mouseReleaseEvent(self, event):
        QGraphicsEllipseItem.mouseReleaseEvent(self, event)  # Call the base class method
        # Update handle positions to reflect the new size
        self.parentItem().updateHandles()