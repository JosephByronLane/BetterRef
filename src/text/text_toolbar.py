# text_toolbar.py

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QSlider, QComboBox, QColorDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase

class TextToolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setStyleSheet("background-color: black;")  # Unified black background
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.editableTextItem = None  # Will be set when a text item is selected

        # Create UI elements
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(10, 10, 10, 10)  # Increased margins for a bigger UI
        h_layout.setSpacing(10)  # Increased spacing between elements

        # Adjust font sizes
        self.button_font_size = 20  # Increased font size for buttons

        # Color button with "A" icon
        self.colorButton = QPushButton("A")
        self.colorButton.setFixedSize(40, 40)  # Increased button size
        self.colorButton.setStyleSheet(
            f"color: white; border: none; font-size: {self.button_font_size}px;")
        self.colorButton.clicked.connect(self.changeTextColor)
        h_layout.addWidget(self.colorButton)

        # Vertical separator
        separator1 = QWidget()
        separator1.setFixedWidth(2)
        separator1.setFixedHeight(40)
        separator1.setStyleSheet("background-color: white;")
        h_layout.addWidget(separator1)

        # Bold button
        self.boldButton = QPushButton("B")
        self.boldButton.setFixedSize(40, 40)
        self.boldButton.setStyleSheet(
            f"color: white; border: none; font-weight: bold; font-size: {self.button_font_size}px;")
        self.boldButton.setCheckable(True)
        self.boldButton.clicked.connect(self.toggleBold)
        h_layout.addWidget(self.boldButton)

        # Italic button
        self.italicButton = QPushButton("I")
        self.italicButton.setFixedSize(40, 40)
        self.italicButton.setStyleSheet(
            f"color: white; border: none; font-style: italic; font-size: {self.button_font_size}px;")
        self.italicButton.setCheckable(True)
        self.italicButton.clicked.connect(self.toggleItalic)
        h_layout.addWidget(self.italicButton)

        # Vertical separator
        separator2 = QWidget()
        separator2.setFixedWidth(2)
        separator2.setFixedHeight(40)
        separator2.setStyleSheet("background-color: white;")
        h_layout.addWidget(separator2)

        # Font size slider
        self.fontSizeSlider = QSlider(Qt.Horizontal)
        self.fontSizeSlider.setMinimum(1)
        self.fontSizeSlider.setMaximum(100)
        self.fontSizeSlider.setValue(12)
        self.fontSizeSlider.setFixedWidth(150)  # Increased width
        self.fontSizeSlider.setFixedHeight(30)  # Increased height
        self.fontSizeSlider.valueChanged.connect(self.changeFontSize)
        h_layout.addWidget(self.fontSizeSlider)

        # Font selector
        self.fontSelector = QComboBox()
        self.fontSelector.setFixedHeight(40)
        self.fontSelector.setStyleSheet("background-color: white; color: black;")
        # Add available fonts
        self.fontSelector.addItems(QFontDatabase().families())
        self.fontSelector.currentIndexChanged.connect(self.changeFont)
        h_layout.addWidget(self.fontSelector)

        self.setLayout(h_layout)

    def setEditableTextItem(self, textItem):
        self.editableTextItem = textItem
        if textItem:
            # Update toolbar UI to match textItem's properties
            font = textItem.font()
            self.fontSizeSlider.setValue(font.pointSize())
            self.boldButton.setChecked(font.bold())
            self.italicButton.setChecked(font.italic())
            # Set font selector to match textItem's font
            index = self.fontSelector.findText(font.family())
            if index >= 0:
                self.fontSelector.setCurrentIndex(index)
            else:
                self.fontSelector.addItem(font.family())
                self.fontSelector.setCurrentIndex(self.fontSelector.count() - 1)
            # Update color button's bar to match text color
            color = textItem.defaultTextColor()
            self.colorButton.setStyleSheet(
                f"color: white; border: none; font-size: {self.button_font_size}px; "
                f"border-bottom: 3px solid {color.name()};")
        else:
            # Clear selections
            self.fontSizeSlider.setValue(12)
            self.boldButton.setChecked(False)
            self.italicButton.setChecked(False)
            self.fontSelector.setCurrentIndex(0)
            self.colorButton.setStyleSheet(
                f"color: white; border: none; font-size: {self.button_font_size}px;")

    def changeTextColor(self):
        if self.editableTextItem:
            color = QColorDialog.getColor()
            if color.isValid():
                self.editableTextItem.setTextColor(color)
                self.colorButton.setStyleSheet(
                    f"color: white; border: none; font-size: {self.button_font_size}px; "
                    f"border-bottom: 3px solid {color.name()};")

    def toggleBold(self):
        if self.editableTextItem:
            self.editableTextItem.toggleBold()
            font = self.editableTextItem.font()
            self.boldButton.setChecked(font.bold())

    def toggleItalic(self):
        if self.editableTextItem:
            self.editableTextItem.toggleItalic()
            font = self.editableTextItem.font()
            self.italicButton.setChecked(font.italic())

    def changeFontSize(self, value):
        if self.editableTextItem:
            self.editableTextItem.setFontSize(value)

    def changeFont(self, index):
        if self.editableTextItem:
            fontFamily = self.fontSelector.currentText()
            font = self.editableTextItem.font()
            font.setFamily(fontFamily)
            self.editableTextItem.setFont(font)
