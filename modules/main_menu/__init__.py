from .main_menu_ui import MainMenuUI  # Import the main UI class
from .settings_handler import SettingsHandler

# Define what will be accessible when importing main_menu
from modules.main_menu.main_menu_ui import MainMenuUI
from modules.main_menu.settings_handler import SettingsHandler

__all__ = ['MainMenuUI', 'SettingsHandler']
