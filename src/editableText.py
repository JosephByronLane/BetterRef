from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem, QMenu, QAction, QColorDialog, QInputDialog, QFontDialog
from PyQt5.QtGui import QFont, QColor, QPen, QTextCursor, QTextCharFormat
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from handle_item import HandleItem
from text.text_toolbar import TextToolbar
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QStyle

class ItemData(QObject):
    dataChanged = pyqtSignal()

class EditableTextItem(QGraphicsTextItem):
    def __init__(self, text="Text", toolbar=None):
        super().__init__(text)
        self.toolbar = toolbar  # Set the toolbar passed as a parameter
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)
        self.itemData = ItemData()
        self.setDefaultTextColor(Qt.white)
        
        self.handles = [HandleItem(self) for _ in range(4)]
        self.hideHandles()
        #self.setSelected(True)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.toolbar and self.isSelected():
            view = self.scene().views()[0]
            pos = view.mapFromScene(self.sceneBoundingRect().topRight())
            global_pos = view.viewport().mapToGlobal(pos)
            self.toolbar.move(global_pos.x(), global_pos.y() - self.toolbar.height())

    def mouseDoubleClickEvent(self, event):
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setFocus()
        self.itemData.dataChanged.emit()

        self.itemData.dataChanged.emit()

        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_B and event.modifiers() == Qt.ControlModifier:
            self.toggleBold()
            return
        elif event.key() == Qt.Key_I and event.modifiers() == Qt.ControlModifier:
            self.toggleItalic()
            return

        super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu()

        # Action to change text color
        colorAction = QAction('Change Text Color...', self)
        colorAction.triggered.connect(self.changeTextColor)
        menu.addAction(colorAction)

        # Action to change font size
        fontSizeAction = QAction('Change Font Size...', self)
        fontSizeAction.triggered.connect(self.changeFontSize)
        menu.addAction(fontSizeAction)

        # Action to change font
        fontAction = QAction('Change Font...', self) 
        fontAction.triggered.connect(self.changeFont)
        menu.addAction(fontAction)

        # Preset colors
        colors = {'Red': QColor('red'), 'Green': QColor('green'), 'Blue': QColor('blue')}
        for name, color in colors.items():
            action = QAction(name, self)
            action.triggered.connect(lambda checked, col=color: self.setTextColor(col))
            menu.addAction(action)

        menu.exec_(event.screenPos())

    def changeTextColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setTextColor(color)

    def changeFontSize(self):
        # Dialog to select font size
        fontSize, ok = QInputDialog.getInt(None, "Font Size", "Enter font size:", min=1, max=100)
        if ok:
            self.setFontSize(fontSize)

    def setFontSize(self, size):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)
        format = cursor.charFormat()
        format.setFontPointSize(size)
        cursor.mergeCharFormat(format)
        self.setTextCursor(cursor)

    def changeFont(self):
        font, ok = QFontDialog.getFont(self.font())
        if ok:
            self.setFont(font)

    def setFont(self, font):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)
        format = cursor.charFormat()
        format.setFontFamily(font.family())
        cursor.mergeCharFormat(format)
        self.setTextCursor(cursor)

    def setTextColor(self, color):
        cursor = self.textCursor()
        if cursor.hasSelection():
            format = cursor.charFormat()
            format.setForeground(color)
            cursor.setCharFormat(format)
        else:
            self.setDefaultTextColor(color)

    def toggleBold(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)
        format = cursor.charFormat()
        weight = format.fontWeight()
        format.setFontWeight(QFont.Bold if weight != QFont.Bold else QFont.Normal)
        cursor.mergeCharFormat(format)
        self.setTextCursor(cursor)

    def toggleItalic(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)
        format = cursor.charFormat()
        format.setFontItalic(not format.fontItalic())
        cursor.mergeCharFormat(format)
        self.setTextCursor(cursor)

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.clearFocus()
        self.setSelected(False)

        super().focusOutEvent(event)

    def boundingRect(self):
        originalRect = super().boundingRect()
        outlineWidth = 3
        return originalRect.adjusted(-outlineWidth, -outlineWidth, outlineWidth, outlineWidth)
    
    def focusOutEvent(self, event):
        # Do not deselect the item when it loses focus
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.clearFocus()
        # Remove or comment out the line below
        # self.setSelected(False)
        super().focusOutEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            if value:
                # Item has been selected
                # Show toolbar
                if self.toolbar:
                    self.toolbar.setEditableTextItem(self)
                    # Position the toolbar near the text item
                    if self.scene() and self.scene().views():
                        view = self.scene().views()[0]  # Assuming one view
                        pos = view.mapFromScene(self.sceneBoundingRect().topRight())
                        global_pos = view.viewport().mapToGlobal(pos)
                        self.toolbar.move(global_pos.x(), global_pos.y() - self.toolbar.height())
                        self.toolbar.show()
            else:
                # Item has been deselected
                # Hide toolbar
                if self.toolbar:
                    self.toolbar.hide()
                    self.toolbar.setEditableTextItem(None)

                # Clear text selection
                cursor = self.textCursor()
                cursor.clearSelection()
                self.setTextCursor(cursor)

                # Optionally remove focus
                self.clearFocus()

        return super().itemChange(change, value)

    def paint(self, painter, option, widget=None):
        # Create a copy of the option and remove the State_HasFocus flag
        option = QStyleOptionGraphicsItem(option)  # Make a copy to avoid modifying the original
        option.state &= ~QStyle.State_HasFocus     # Remove the focus state

        # Call the superclass paint method with the modified option
        super().paint(painter, option, widget)

        # Custom selection rectangle (if needed)
        if self.isSelected():
            painter.setPen(QPen(QColor('blue'), 3))
            painter.drawRect(self.boundingRect().adjusted(3, 3, -3, -3))

    def updateHandles(self):
        if not self.isSelected():
            for handle in self.handles:
                handle.hide()
            return

        rect = self.boundingRect()
        corners = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]

        for handle, pos in zip(self.handles, corners):
            handle.setPos(self.mapToScene(pos))
            handle.show()

    def hideHandles(self):
        for handle in self.handles:
            handle.hide()

    def showHandles(self):
        self.updateHandles()
        for handle in self.handles:
            handle.show()
