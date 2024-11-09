from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QStackedWidget, QMainWindow, QPushButton , QFrame
from PyQt5.QtCore import Qt, QPoint

class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        main_layout = QHBoxLayout(self)

        # Sidebar (left panel with list items)
        self.sidebar = QListWidget()
        self.sidebar.setFocusPolicy(Qt.NoFocus)
        self.sidebar.setFixedWidth(150)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2D2D2D;
                color: #AAAAAA;
                border: none;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #3A3A3A;
                color: #FFFFFF;
                outline: 0;  /* Remove dotted outline */
            }
            QListWidget::item:focus {
                outline: 0;  /* Remove focus outline */
            }
        """)

        self.add_sidebar_item("Preferences")
        self.add_sidebar_item("Account")
        self.add_sidebar_item("Notifications")
        self.add_sidebar_item("Privacy")

        separator = QFrame()
        separator.setFixedWidth(2)  # Set the width of the separator
        separator.setStyleSheet("background-color: #5F5F5F;")  # Set the color of the separator

        # Stack widget for the content (right panel)
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #2D2D2D; border: none;")

        # Example content for each settings page
        self.content_stack.addWidget(self.create_settings_page("Preferences"))
        self.content_stack.addWidget(self.create_settings_page("Account"))
        self.content_stack.addWidget(self.create_settings_page("Notifications"))
        self.content_stack.addWidget(self.create_settings_page("Privacy"))

        # Connect sidebar selection to stack widget display
        self.sidebar.currentRowChanged.connect(self.display_content)

        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(separator)  # Add the separator between sidebar and main content

        main_layout.addWidget(self.content_stack)
        self.setLayout(main_layout)

    def add_sidebar_item(self, text):
        """Adds an item to the sidebar with the specified text."""
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)  # Align items to the left and vertically center
        self.sidebar.addItem(item)

    def create_settings_page(self, title):
        """Creates a placeholder page with the specified title for each setting."""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(title)
        label.setStyleSheet("color: #FFFFFF; font-size: 24px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    def display_content(self, index):
        """Switches to the content page corresponding to the selected sidebar item."""
        self.content_stack.setCurrentIndex(index)


class CustomSettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint )
        self.setWindowTitle("Settings")
        
        # Initialize variables for dragging
        self.drag_position = None

        # Remove window borders and add a custom title bar
        self.setStyleSheet("background-color: #2D2D2D; border: none;")

        # Custom title bar layout
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #2D2D2D; padding-bottom: 5px;")

        # Title bar layout with title and close button
        title_bar_layout = QHBoxLayout(title_bar)
        title_label = QLabel("Settings")
        title_label.setStyleSheet("color: #FFFFFF; font-size: 16px; padding-left: 10px;")
        title_label.setAlignment(Qt.AlignCenter)

        # Custom close button
        close_button = QPushButton("X")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: #2D2D2D;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FF5C5C;
            }
        """)
        close_button.clicked.connect(self.close)

        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(close_button)

        # Main layout with title bar and settings content
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_bar)
        main_layout.addWidget(SettingsMenu(self))

        # Container widget for the window layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Set a reasonable size for the settings window
        self.resize(800, 600)

    def mousePressEvent(self, event):
        """Detects right mouse button press to start dragging the window."""
        if event.button() == Qt.RightButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Moves the entire window when the right mouse button is held and moved."""
        if event.buttons() & Qt.RightButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Clears drag position when right mouse button is released."""
        if event.button() == Qt.RightButton:
            self.drag_position = None
            event.accept()


def show_settings_window():
    """Displays the settings window."""
    settings_window = CustomSettingsWindow()
    settings_window.show()
    return settings_window
