from context_menu.context_menu_entries import create_context_menu_entries
from context_menu.context_menu import CustomContextMenu

def show_context_menu(parent, context_menu_position):
    """Displays a context menu at the specified position."""
    if context_menu_position:
        menu = CustomContextMenu(parent)
        
        # Use the external function to create entries, passing the parent widget
        entries = create_context_menu_entries(parent)
        menu.populate_context_menu(entries)
        
        # Show the context menu at the given position
        menu.exec_(context_menu_position)