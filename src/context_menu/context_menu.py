from PyQt5.QtWidgets import QMenu, QWidgetAction

class CustomContextMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QMenu {
                background-color: #222222;  /* Dark background color */
                color: #FFFFFF;  /* Text color */
                
                padding: 5px;
            }
            QMenu::item {
                background-color: transparent;  /* Transparent background */
                padding: 5px 15px;  /* Add padding for menu items */
            }
            QMenu::item:selected {
                background-color: #FFFFFF;  /* Background color when hovered */
            }
            QMenu::separator {
                height: 2px;  /* Line height */
                background: #FFFFFF;  /* White line color */
                margin: 5px 10px;  /* Margin to add spacing */
            }
        """)

    def populate_context_menu(self, entries):
        """Populate the context menu with the provided entries."""
        for i, entry_widget in enumerate(entries):  # Use enumerate directly on the list of entries
            widget_action = QWidgetAction(self)
            widget_action.setDefaultWidget(entry_widget)  # Embed the custom entry widget
            widget_action.triggered.connect(entry_widget.action)

            self.addAction(widget_action)

            # Add a separator after specific entries (e.g., after 'Copy' and 'Paste')
            if i == 1:  # Adjust the index as needed to add separators after specific items
                self.addSeparator()