from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QComboBox, QColorDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont

class TextToolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: black;")
        self.setFocusPolicy(Qt.NoFocus)

        self.editableTextItem = None  # Will be set when a text item is selected

        # Check if 'Inter' font is available
        font_db = QFontDatabase()
        if 'Inter' in font_db.families():
            inter_font_family = 'Inter'
        else:
            inter_font_family = self.font().family()  # Use default font

        # Create UI elements
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(10, 10, 10, 10)  # Increased margins for a bigger UI
        h_layout.setSpacing(10)  # Increased spacing between elements

        # Adjust font sizes
        self.button_font_size = 20  # Font size for buttons

        # Color button with "A" icon
        self.colorButton = QPushButton("A")
        self.colorButton.setFixedSize(40, 40)
        self.colorButton.setStyleSheet(
            f"""
            QPushButton {{
                color: white;
                border: none;
                font-size: {self.button_font_size}px;
            }}
            """)
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
        self.boldButton.setCheckable(True)
        self.boldButton.setStyleSheet(
            f"""
            QPushButton {{
                color: white;
                border: none;
                font-weight: bold;
                font-size: {self.button_font_size}px;
            }}
            QPushButton:checked {{
                background-color: blue;
                color: white;
            }}
            """)
        self.boldButton.clicked.connect(self.toggleBold)
        h_layout.addWidget(self.boldButton)

        # Italic button
        self.italicButton = QPushButton("I")
        self.italicButton.setFixedSize(40, 40)
        self.italicButton.setCheckable(True)
        self.italicButton.setStyleSheet(
            f"""
            QPushButton {{
                color: white;
                border: none;
                font-style: italic;
                font-size: {self.button_font_size}px;
            }}
            QPushButton:checked {{
                background-color: blue;
                color: white;
            }}
            """)
        self.italicButton.clicked.connect(self.toggleItalic)
        h_layout.addWidget(self.italicButton)

        # Vertical separator
        separator2 = QWidget()
        separator2.setFixedWidth(2)
        separator2.setFixedHeight(40)
        separator2.setStyleSheet("background-color: white;")
        h_layout.addWidget(separator2)

        # Font size dropdown
        self.fontSizeComboBox = QComboBox()
        self.fontSizeComboBox.setFixedHeight(40)
        self.fontSizeComboBox.setEditable(True)
        self.fontSizeComboBox.setFont(QFont(inter_font_family))
        self.fontSizeComboBox.setStyleSheet(
            f"""
            QComboBox {{
                background-color: #222222;
                color: white;
                border: none;
                font-family: {inter_font_family};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                width: 0;
                height: 0;
            }}
            QComboBox QAbstractItemView {{
                background-color: #222222;
                color: white;
                selection-background-color: #333333;
                border: none;
                font-family: {inter_font_family};
            }}
            QComboBox QAbstractItemView QScrollBar:vertical {{
                background: #2e2e2e;
                width: 10px;
            }}
            QComboBox QAbstractItemView QScrollBar::handle:vertical {{
                background: #4d4d4d;
                min-height: 20px;
            }}
            QComboBox QAbstractItemView QScrollBar::add-line:vertical,
            QComboBox QAbstractItemView QScrollBar::sub-line:vertical {{
                background: none;
                height: 0px;
            }}
            QComboBox QAbstractItemView QScrollBar::up-arrow:vertical,
            QComboBox QAbstractItemView QScrollBar::down-arrow:vertical {{
                background: none;
            }}
            """)
        # Common font sizes
        font_sizes = [
            '8', '9', '10', '11', '12', '14', '16', '18', '20',
            '22', '24', '26', '28', '36', '48', '72'
        ]
        self.fontSizeComboBox.addItems(font_sizes)
        self.fontSizeComboBox.setCurrentText('12')
        self.fontSizeComboBox.currentIndexChanged.connect(self.changeFontSize)
        self.fontSizeComboBox.lineEdit().editingFinished.connect(self.changeFontSize)
        h_layout.addWidget(self.fontSizeComboBox)

        # Font selector
        self.fontSelector = QComboBox()
        self.fontSelector.setFixedHeight(40)
        self.fontSelector.setFont(QFont(inter_font_family))
        self.fontSelector.setStyleSheet(
            f"""
            QComboBox {{
                background-color: #222222;
                color: white;
                border: none;
                font-family: {inter_font_family};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                width: 0;
                height: 0;
            }}
            QComboBox QAbstractItemView {{
                background-color: #222222;
                color: white;
                selection-background-color: #333333;
                border: none;
                font-family: {inter_font_family};
            }}
            QComboBox QAbstractItemView QScrollBar:vertical {{
                background: #2e2e2e;
                width: 10px;
            }}
            QComboBox QAbstractItemView QScrollBar::handle:vertical {{
                background: #4d4d4d;
                min-height: 20px;
            }}
            QComboBox QAbstractItemView QScrollBar::add-line:vertical,
            QComboBox QAbstractItemView QScrollBar::sub-line:vertical {{
                background: none;
                height: 0px;
            }}
            QComboBox QAbstractItemView QScrollBar::up-arrow:vertical,
            QComboBox QAbstractItemView QScrollBar::down-arrow:vertical {{
                background: none;
            }}
            """)
        # Add available fonts
        self.fontSelector.addItems(QFontDatabase().families())
        self.fontSelector.currentIndexChanged.connect(self.changeFont)
        h_layout.addWidget(self.fontSelector)

        # Set focus policy for all child widgets
        self.colorButton.setFocusPolicy(Qt.NoFocus)
        self.boldButton.setFocusPolicy(Qt.NoFocus)
        self.italicButton.setFocusPolicy(Qt.NoFocus)


        self.setLayout(h_layout)
    def focusOutEvent(self, event):
        # Do not deselect the item when it loses focus
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.clearFocus()
        # Comment out or remove the line below
        # self.setSelected(False)
        super().focusOutEvent(event)

    def setEditableTextItem(self, textItem):
        self.editableTextItem = textItem
        if textItem:
            # Update toolbar UI to match textItem's properties
            cursor = textItem.textCursor()
            format = cursor.charFormat()

            # Update font size
            font_size = format.fontPointSize()
            if font_size > 0:
                self.fontSizeComboBox.setCurrentText(str(int(font_size)))
            else:
                self.fontSizeComboBox.setCurrentText('12')

            # Update bold and italic buttons
            self.boldButton.setChecked(format.fontWeight() == QFont.Bold)
            self.italicButton.setChecked(format.fontItalic())

            # Update font family
            font_family = format.fontFamily()
            index = self.fontSelector.findText(font_family)
            if index >= 0:
                self.fontSelector.setCurrentIndex(index)
            else:
                self.fontSelector.addItem(font_family)
                self.fontSelector.setCurrentIndex(self.fontSelector.count() - 1)

            # Update color button's bar to match text color
            color = format.foreground().color()
            self.colorButton.setStyleSheet(
                f"""
                QPushButton {{
                    color: white;
                    border: none;
                    font-size: {self.button_font_size}px;
                    border-bottom: 3px solid {color.name()};
                }}
                """)
        else:
            # Clear selections
            self.fontSizeComboBox.setCurrentText('12')
            self.boldButton.setChecked(False)
            self.italicButton.setChecked(False)
            self.fontSelector.setCurrentIndex(0)
            self.colorButton.setStyleSheet(
                f"""
                QPushButton {{
                    color: white;
                    border: none;
                    font-size: {self.button_font_size}px;
                }}
                """)

    def changeTextColor(self):
        if self.editableTextItem:
            color = QColorDialog.getColor()
            if color.isValid():
                self.editableTextItem.setTextColor(color)
                self.colorButton.setStyleSheet(
                    f"""
                    QPushButton {{
                        color: white;
                        border: none;
                        font-size: {self.button_font_size}px;
                        border-bottom: 3px solid {color.name()};
                    }}
                    """)

    def toggleBold(self):
        if self.editableTextItem:
            self.editableTextItem.toggleBold()
            # Update the button's checked state
            cursor = self.editableTextItem.textCursor()
            format = cursor.charFormat()
            self.boldButton.setChecked(format.fontWeight() == QFont.Bold)

    def toggleItalic(self):
        if self.editableTextItem:
            self.editableTextItem.toggleItalic()
            # Update the button's checked state
            cursor = self.editableTextItem.textCursor()
            format = cursor.charFormat()
            self.italicButton.setChecked(format.fontItalic())

    def changeFontSize(self):
        if self.editableTextItem:
            # Get the font size from the combo box
            font_size_text = self.fontSizeComboBox.currentText()
            try:
                font_size = int(font_size_text)
                self.editableTextItem.setFontSize(font_size)
            except ValueError:
                pass  # Ignore invalid input

    def changeFont(self, index):
        if self.editableTextItem:
            fontFamily = self.fontSelector.currentText()
            font = self.editableTextItem.font()
            font.setFamily(fontFamily)
            self.editableTextItem.setFont(font)
