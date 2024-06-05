from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import pyqtSignal, QObject, Qt

class ItemData(QObject):
    dataChanged = pyqtSignal()


class EditableTextItem(QGraphicsTextItem):
    def __init__(self, text="Text"):
        super().__init__(text)
        self.itemData = ItemData()
        self.setDefaultTextColor(Qt.white)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)  
        
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

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
                self.itemData.dataChanged.emit()
        return super().itemChange(change, value)