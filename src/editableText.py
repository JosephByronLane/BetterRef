from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem
from PyQt5.QtGui import QFont, QColor, QPen, QCursor
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QPointF
from handle_item import HandleItem

class ItemData(QObject):
    dataChanged = pyqtSignal()


class EditableTextItem(QGraphicsTextItem):
    def __init__(self, text="Text"):
        super().__init__(text)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)
        self.itemData = ItemData()
        self.setDefaultTextColor(Qt.white) 

        self.handles = [HandleItem(self) for _ in range(4)] 
        self.hideHandles()  

    def mouseDoubleClickEvent(self, event):
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setFocus()
        self.itemData.dataChanged.emit()

        super().mouseDoubleClickEvent(event)

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.clearFocus()  
        self.setSelected(False) 
        
        super().focusOutEvent(event)

    def boundingRect(self):
        originalRect = super().boundingRect()
        outlineWidth = 3  
        return originalRect.adjusted(-outlineWidth, -outlineWidth, outlineWidth, outlineWidth)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.itemData.dataChanged.emit()
        elif change == QGraphicsItem.ItemSelectedHasChanged:
            if value:
                self.showHandles()
            else:
                self.hideHandles()
        return super().itemChange(change, value)
    
    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setPen(QPen(QColor('blue'), 3))
            painter.drawRect(self.boundingRect().adjusted(3, 3, -3, -3))

    def updateHandles(self):
        if not self.isSelected():
            for handle in self.handles:
                handle.hide()
            return

        rect = self.boundingRect()
        print(f"Bounding Rect: {rect}")
        corners = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]
        print(f"corners: {corners}")

        for handle, pos in zip(self.handles, corners):
            print(f"Handle tobe- pos: {pos}")
            handle.setPos(self.mapToScene(pos))
            print(f"Handle Position: {handle.pos()}")
            handle.show()

    def hideHandles(self):
        for handle in self.handles:
            handle.hide()

    def showHandles(self):
        self.updateHandles()
        for handle in self.handles:
            handle.show()