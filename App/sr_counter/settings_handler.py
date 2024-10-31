import json, os
from PyQt6.QtWidgets import QMessageBox
from dialogs.settings_dialog import SettingsDialog
from utils.app_settings import AppSettings  # Import the global AppSettings
from utils.file_helpers import FileHelper  # Import the FileHelper class

class SettingsHandler:
    def __init__(self, parent):
        self.parent = parent
        self.config_path = FileHelper.resource_path('settings.json')  # Use FileHelper to get the config path
        self.app_settings = AppSettings()  # Instantiate the global AppSettings

    def open_settings_dialog(self):
        """Open the settings dialog related to SR Counter exclusions."""
        try:
            json_path = FileHelper.get_json_file_path('type_group_exclusion.json')
            with open(json_path, 'r') as f:
                data = json.load(f)
            sr_types = data.get("type_descriptions", {})
            group_descriptions = data.get("group_descriptions", {})
            
            # Pass data to the SettingsDialog
            dialog = SettingsDialog(self.parent, sr_types, group_descriptions)
            if dialog.exec():  # If user clicked OK (Dialog accepted)
                exclusions = dialog.get_exclusions()  # Get exclusions from the dialog
                self.save_exclusion_settings(
                    exclusions['excluded_sr_type'], 
                    exclusions['excluded_group'], 
                    exclusions.get('no_location_sr_type', []), 
                    exclusions.get('no_location_group', [])
                )
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error loading JSON: {e}")

    def save_exclusion_settings(self, sr_type_exclusions, group_exclusions, no_location_sr_exclusions, no_location_group_exclusions):
        """Saves exclusion settings for SR types and groups without overwriting other settings."""
        # Use global AppSettings to retrieve and save the current settings
        current_settings = self.app_settings.load_settings()

        # Update the exclusions part of the settings
        current_settings["exclusions"]["excluded_sr_type"] = sr_type_exclusions
        current_settings["exclusions"]["excluded_group"] = group_exclusions
        current_settings["exclusions"]["no_location_sr_type"] = no_location_sr_exclusions
        current_settings["exclusions"]["no_location_group"] = no_location_group_exclusions

        # Save the updated settings back to the file
        self.app_settings.save_settings(current_settings)

        print("Exclusion settings updated successfully.")
