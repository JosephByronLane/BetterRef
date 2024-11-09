from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QColorDialog
from PyQt5.QtGui import QColor

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.layout = QVBoxLayout(self)

        self.colorButton = QPushButton("Select Widget Color")
        self.colorButton.clicked.connect(self.selectColor)
        self.layout.addWidget(self.colorButton)

        self.selectedColor = QColor('blue')  # Default color

    def selectColor(self):
        color = QColorDialog.getColor(self.selectedColor, self, "Select Widget Color")
        if color.isValid():
            self.selectedColor = color
