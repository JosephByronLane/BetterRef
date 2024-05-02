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
        QGraphicsEllipseItem.mouseMoveEvent(self, event)  # Call the base class method

        # Calculate the current mouse position in the scene coordinates
        currentPos = self.mapToScene(event.pos())
        # Calculate the delta from the starting position to the current position
        delta = currentPos - self.startPos

        # Calculate vectors from the center of the parent item
        center = self.parentItem().sceneBoundingRect().center()
        startVector = self.startPos - center
        currentVector = currentPos - center

        # Calculate scaling factor based on the length of vectors
        if startVector.manhattanLength() != 0:
            scaleFactor = currentVector.manhattanLength() / startVector.manhattanLength()
        else:
            scaleFactor = .5

        # Correcting scale sensitivity by adjusting the scale factor calculation
        scaleFactor = 1 + (scaleFactor - 1) / 2  # Adjust this factor to tune sensitivity

        # Set the scale with the center as the anchor point
        self.parentItem().setTransformOriginPoint(self.parentItem().boundingRect().width() / 2, self.parentItem().boundingRect().height() / 2)
        self.parentItem().setScale(self.startScale * scaleFactor)

        # Emit the dataChanged signal to update any bindings or save changes
        self.parentItem().itemData.dataChanged.emit()

    def mouseReleaseEvent(self, event):
        self.parentItem().updateHandles() 
        super().mouseReleaseEvent(event)

    def mouseReleaseEvent(self, event):
        QGraphicsEllipseItem.mouseReleaseEvent(self, event)  # Call the base class method
        # Update handle positions to reflect the new size
        self.parentItem().updateHandles()