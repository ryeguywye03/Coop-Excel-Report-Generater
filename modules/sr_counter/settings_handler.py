import json
from PyQt6.QtWidgets import QMessageBox
from modules.dialogs.settings_dialog import SettingsDialog
from modules.utils.file_helpers import FileHelper
from modules.utils.app_settings import AppSettings  # Import the global AppSettings
from modules.utils.logger_manager import LoggerManager  # Import the LoggerManager class

class SettingsHandler:
    def __init__(self, parent):
        self.parent = parent
        self.config_path = FileHelper.get_settings_file_path()  # Use FileHelper to get the config path
        self.app_settings = AppSettings()  # Instantiate the global AppSettings
        self.logger = LoggerManager(enable_logging=True)  # Initialize the logger

    def open_settings_dialog(self):
        """Open the settings dialog related to SR Counter exclusions."""
        try:
            json_path = FileHelper.get_json_file_path('type_group_exclusion.json')
            with open(json_path, 'r') as f:
                data = json.load(f)

            # Check if data is None and log an error if it is
            if data is None:
                self.logger.log_error("Loaded JSON data is None. Please check the JSON file.")
                QMessageBox.critical(self.parent, "Error", "Error loading JSON: JSON file is empty or corrupted.")
                return

            # Ensure `data` is a dictionary before attempting to access its keys
            if not isinstance(data, dict):
                raise TypeError(f"Expected data to be a dictionary, but got {type(data)}")

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
            self.logger.log_error(f"Error loading JSON: {e}")
            QMessageBox.critical(self.parent, "Error", f"Error loading JSON: {e}")



    def save_exclusion_settings(self, sr_type_exclusions, group_exclusions, no_location_sr_exclusions, no_location_group_exclusions, no_location_included_sr_exclusions, no_location_included_group_exclusions, enable_states):
        """Saves exclusion settings for SR types, groups, and new no location settings with IDs without overwriting other settings."""
        current_settings = self.app_settings.load_settings()
        exclusions = current_settings.get("exclusions", {})

        # Expect lists of IDs for exclusions instead of dictionaries
        exclusions["excluded_sr_type"] = sr_type_exclusions
        exclusions["excluded_group"] = group_exclusions
        exclusions["no_location_excluded_sr_type"] = no_location_sr_exclusions
        exclusions["no_location_excluded_group"] = no_location_group_exclusions
        exclusions["no_location_included_sr_type"] = no_location_included_sr_exclusions
        exclusions["no_location_included_group"] = no_location_included_group_exclusions

        # Debug log for enable states
        for key, value in enable_states.items():
            self.logger.log_debug(f"Enable state for {key}: {value}")
        
        # Add enable states to exclusions
        exclusions.update(enable_states)

        # Assign the updated exclusions back to the settings
        current_settings["exclusions"] = exclusions

        # Save the updated settings back to the file
        self.app_settings.save_settings(current_settings)
        self.logger.log_info("Exclusion settings updated successfully.")
