from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class ContextMenuEntry(QWidget):
    def __init__(self, name, keybind, action, parent=None):
        super().__init__(parent)

        # Store the action for later execution
        self.action = action

        # Set up the layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Create and style the name label
        self.name_label = QLabel(name, self)
        self.name_label.setStyleSheet("color: #AAAAAA; font-size: 14px;")  # Custom color and font size
        self.name_label.setAlignment(Qt.AlignLeft)

        # Create and style the keybind label
        self.keybind_label = QLabel(keybind, self)
        self.keybind_label.setStyleSheet("color: #5F5F5F; font-size: 14px;")  # Custom color and font size
        self.keybind_label.setAlignment(Qt.AlignRight)

        # Add labels to the layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.keybind_label)

        # Set the layout
        self.setLayout(layout)

    def trigger_action(self):
        """Execute the assigned action when called."""
        if callable(self.action):
            self.action()