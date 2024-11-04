# context_menu/context_menu_entries.py

from context_menu.context_menu_entry import ContextMenuEntry  # Import the entry widget class

def create_context_menu_entries(parent):
    """Create a list of ContextMenuEntry widgets."""
    copy_action = lambda: print("Copy action executed")  # Replace with actual logic
    paste_action = lambda: print("Paste action executed")  # Replace with actual logic
    settings_action = lambda: print("Settings action executed")  # Replace with actual logic

    # Instantiate ContextMenuEntry widgets
    copy_entry = ContextMenuEntry("Copy", "CTRL + C", copy_action, parent)
    paste_entry = ContextMenuEntry("Paste", "CTRL + V", paste_action, parent)
    settings_entry = ContextMenuEntry("Settings", "CTRL + U", settings_action, parent)

##TODO: make this automated, adding a for loop to iterate over every contextMenuEntry and return that

    # Return the entries in the order they should appear
    return [copy_entry, paste_entry, settings_entry]
