# context_menu/context_menu_entries.py

from context_menu.context_menu_entry import ContextMenuEntry  # Import the entry widget class
from settings_menu.settings_menu import show_settings_window
def create_context_menu_entries(parent):
    """Create a list of ContextMenuEntry widgets."""
    copy_action = lambda: print("Copy action executed")  # Replace with actual logic
    paste_action = lambda: print("Paste action executed")  # Replace with actual logic
    settings_action = lambda: globals().update(settings_window=show_settings_window())
    cut_action = lambda: print("Cut action executed")  # Replace with actual logic
    text_action = lambda: print("Text action executed")  # Replace with actual logic
    open_action = lambda: print("Open action executed")  # Replace with actual logic
    save_action = lambda: print("Save action executed")  # Replace with actual logic

    spacer = ContextMenuEntry("Spacer", "", None, parent)


    # Instantiate ContextMenuEntry widgets
    settings_entry = ContextMenuEntry("Settings", "CTRL + U", settings_action, parent)

    copy_entry = ContextMenuEntry("Copy", "CTRL + C", copy_action, parent)
    paste_entry = ContextMenuEntry("Paste", "CTRL + V", paste_action, parent)
    cut_entry = ContextMenuEntry("Cut", "CTRL + X", cut_action, parent)
    text_entry = ContextMenuEntry("Text", "T", text_action, parent)
    open_entry = ContextMenuEntry("Open File", "CTRL + O", open_action, parent)
    save_entry = ContextMenuEntry("Save File", "CTRL + S", save_action, parent)

##TODO: make this automated, adding a for loop to iterate over every contextMenuEntry and return that

    return [settings_entry, spacer, copy_entry, paste_entry, cut_entry, spacer, text_entry, spacer, open_entry, save_entry]
