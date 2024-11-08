import json
import os
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
                exclusions = dialog.get_exclusions()  # Get exclusions and enable states from the dialog
                self.save_exclusion_settings(
                    exclusions['excluded_sr_type'], 
                    exclusions['excluded_group'], 
                    exclusions.get('no_location_excluded_sr_type', []), 
                    exclusions.get('no_location_excluded_group', []), 
                    exclusions.get('no_location_included_sr_type', []), 
                    exclusions.get('no_location_included_group', []), 
                    enable_states={
                        "enable_excluded_sr_type": exclusions.get('enable_excluded_sr_type', False),
                        "enable_excluded_group": exclusions.get('enable_excluded_group', False),
                        "enable_no_location_excluded_sr_type": exclusions.get('enable_no_location_excluded_sr_type', False),
                        "enable_no_location_excluded_group": exclusions.get('enable_no_location_excluded_group', False),
                        "enable_no_location_included_sr_type": exclusions.get('enable_no_location_included_sr_type', False),
                        "enable_no_location_included_group": exclusions.get('enable_no_location_included_group', False),
                    }
                )
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error loading JSON: {e}")

    def save_exclusion_settings(self, sr_type_exclusions, group_exclusions, no_location_sr_exclusions, no_location_group_exclusions, no_location_included_sr_exclusions, no_location_included_group_exclusions, enable_states):
        """Saves exclusion settings for SR types, groups, and new no location settings with IDs without overwriting other settings."""
        # Use global AppSettings to retrieve and save the current settings
        current_settings = self.app_settings.load_settings()

        # Update only non-empty values to avoid overwriting existing settings unintentionally
        exclusions = current_settings.get("exclusions", {})

        # Map exclusions to use IDs
        if sr_type_exclusions:
            exclusions["excluded_sr_type"] = [{"id": sr_id, "description": description} for sr_id, description in sr_type_exclusions.items()]
        if group_exclusions:
            exclusions["excluded_group"] = [{"id": group_id, "description": description} for group_id, description in group_exclusions.items()]
        if no_location_sr_exclusions:
            exclusions["no_location_excluded_sr_type"] = [{"id": sr_id, "description": description} for sr_id, description in no_location_sr_exclusions.items()]
        if no_location_group_exclusions:
            exclusions["no_location_excluded_group"] = [{"id": group_id, "description": description} for group_id, description in no_location_group_exclusions.items()]
        if no_location_included_sr_exclusions:
            exclusions["no_location_included_sr_type"] = [{"id": sr_id, "description": description} for sr_id, description in no_location_included_sr_exclusions.items()]
        if no_location_included_group_exclusions:
            exclusions["no_location_included_group"] = [{"id": group_id, "description": description} for group_id, description in no_location_included_group_exclusions.items()]

        # Add enable states to exclusions
        exclusions.update(enable_states)

        # Assign the updated exclusions back to the settings
        current_settings["exclusions"] = exclusions

        # Save the updated settings back to the file
        self.app_settings.save_settings(current_settings)
        print("Exclusion settings updated successfully.")
