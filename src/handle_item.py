from PyQt5.QtGui import QColor, QPen, QTransform, QCursor
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import Qt

class HandleItem(QGraphicsEllipseItem):
    def __init__(self, parent=None, canvas=None):
        super().__init__(-10, -10, 20, 20, parent)
        self.setBrush(QColor('blue'))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(100)
        self.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.canvas = canvas

    def canvas(self):
        return self.canvas
    def mousePressEvent(self, event):
        QGraphicsEllipseItem.mousePressEvent(self, event)
        self.startPos = self.scenePos()
        self.startTransform = self.parentItem().transform()
        self.originalSize = self.parentItem().boundingRect().size()

        # Disable movement of the parent item
        self.parentItem().setFlag(QGraphicsItem.ItemIsMovable, False)

    def mouseMoveEvent(self, event):
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

        transform = QTransform.fromScale(scaleFactor, scaleFactor)
        self.parentItem().setTransform(self.startTransform * transform, False)

        if hasattr(self.parentItem(), 'updateHandles'):
            self.parentItem().updateHandles()
            
        self.parentItem().itemData.dataChanged.emit()

    def mouseReleaseEvent(self, event):
        QGraphicsEllipseItem.mouseReleaseEvent(self, event) 

        self.parentItem().setFlag(QGraphicsItem.ItemIsMovable, True)

        if hasattr(self.parentItem(), 'updateGroupHandles'):
            self.parentItem().updateGroupHandles()
        else:
            self.parentItem().updateHandles()


    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setBrush(self.parentItem().canvas().settingsWindow.selectedColor)
            painter.setPen(QPen(QColor('blue'), 3))           
            painter.drawRect(self.boundingRect())
   
    def updateHandles(self):
        rect = self.parentItem().boundingRect()
        corners = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]
        for handle, pos in zip(self.parentItem().handles, corners):
            handle.setPos(self.parentItem().mapToScene(pos))

        rect = self.boundingRect()
        corners = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]
        for handle, pos in zip(self.handles, corners):
            handle.setPos(self.mapToScene(pos))
            handle.show()