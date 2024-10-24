from PyQt5.QtWidgets import QMessageBox
from dialogs.settings_dialog import SettingsDialog
from utils.settings_manager import SettingsManager

class SettingsHandler:
    def __init__(self, parent):
        self.parent = parent
        self.settings_manager = SettingsManager()

    def open_settings_dialog(self):
        """Open the settings dialog related to SR Counter exclusions."""
        try:
            # Load settings using SettingsManager
            settings = self.settings_manager.load_settings()

            # Pass data to the SettingsDialog
            dialog = SettingsDialog(self.parent, settings['excluded_sr_type'], settings['excluded_group'])

            # If user clicks OK (dialog accepted), save settings
            if dialog.exec_():
                exclusions = dialog.get_exclusions()
                self.save_exclusion_settings(exclusions)
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error loading settings: {e}")

    def save_exclusion_settings(self, exclusions):
        """Saves exclusion settings for SR types and groups."""
        try:
            # Save the updated settings using SettingsManager
            self.settings_manager.save_settings(exclusions)
            print("Exclusion settings saved.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error saving settings: {e}")
