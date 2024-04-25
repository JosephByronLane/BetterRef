from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QMouseEvent
from handle_item import HandleItem
from PyQt5.QtCore import pyqtSignal, QObject

class ItemData(QObject):
    dataChanged = pyqtSignal()


class SelectableImageItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.handles = [HandleItem(self) for _ in range(4)]  
        for handle in self.handles:
            handle.hide()
        self.itemData = ItemData()

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setPen(QPen(QColor('blue'), 3))  
            painter.drawRect(self.boundingRect())


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            #simplemente hereda la implementacion default de QMouseEvent, de momento no hay que cambiarle.
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)
            self.itemData.dataChanged.emit()

        super().mouseReleaseEvent(event)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setPen(QPen(QColor('blue'), 3))
            painter.drawRect(self.boundingRect())

    def updateHandles(self):
        if self.isSelected() and not self.handles:
            for _ in range(4):  
                handle = HandleItem(self)
                self.handles.append(handle)
            self.positionHandles()
        elif not self.isSelected():
            for handle in self.handles:
                self.scene().removeItem(handle)
            self.handles.clear()
        else:
            self.positionHandles() 

    def positionHandles(self):
        rect = self.boundingRect()
        self.handles[0].setPos(rect.topLeft())
        self.handles[1].setPos(rect.topRight())
        self.handles[2].setPos(rect.bottomRight())
        self.handles[3].setPos(rect.bottomLeft())

    def itemChange(self, change, value):
            if change == QGraphicsItem.ItemSelectedHasChanged:
                if value:  
                    self.positionHandles()  
                    for handle in self.handles:
                        handle.show()  
                else:  
                    for handle in self.handles:
                        handle.hide() 
            return super().itemChange(change, value)