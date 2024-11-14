import json
import os
from .file_helpers import FileHelper
from .logger_manager import LoggerManager

class AppSettings:
    def __init__(self):
        # Initialize logger
        self.logger = LoggerManager()

        # Set the config file path using FileHelper
        self.config_file = FileHelper.get_settings_file_path()

        # Ensure the config file is ready
        self.prepare_config_file()

        # Load settings or initialize defaults
        self.settings = self.load_settings()

    def prepare_config_file(self):
        """Ensures that the settings file exists within the designated path."""
        config_dir = os.path.dirname(self.config_file)
        
        # Ensure the directory exists
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir, exist_ok=True)
                self.logger.log_debug(f"Created config directory at {config_dir}")
            except OSError as e:
                self.logger.log_error(f"Failed to create config directory {config_dir}: {e}")

        # Create a default settings file if it doesn't exist
        if not os.path.exists(self.config_file):
            self.logger.log_debug(f"No settings file found. Creating default settings at {self.config_file}")
            self.settings = self.default_settings()
            self.save_settings(self.settings)

    def load_settings(self):
        """Loads settings from the JSON file or returns defaults if the file is empty/corrupt."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    settings = json.load(f)
                    if not settings:
                        self.logger.log_debug("Settings file is empty. Initializing with default settings.")
                        return self.default_settings()
                    self.logger.log_info("Settings loaded successfully.")
                    return settings
            except json.JSONDecodeError as e:
                self.logger.log_error(f"JSON decode error in {self.config_file}: {e}. Reverting to default settings.")
                os.remove(self.config_file)  # Remove the corrupt file
                self.settings = self.default_settings()
                self.save_settings(self.settings)  # Recreate the file with default settings
                return self.settings
            except IOError as e:
                self.logger.log_error(f"Error reading settings file {self.config_file}: {e}")
                return self.default_settings()
        else:
            self.logger.log_debug(f"No settings file found. Creating default settings at {self.config_file}.")
            return self.default_settings()

    def default_settings(self):
        """Returns the default settings."""
        default = {
            "theme": "dark",
            "window_size": {"width": 1000, "height": 600},
            "exclusions": {
                "excluded_sr_type": [],
                "excluded_group": [],
                "no_location_excluded_sr_type": [],
                "no_location_excluded_group": [],
                "no_location_included_sr_type": [],
                "no_location_included_group": [],
                "enable_excluded_sr_type": False,
                "enable_excluded_group": False,
                "enable_no_location_excluded_sr_type": False,
                "enable_no_location_excluded_group": False,
                "enable_no_location_included_sr_type": False,
                "enable_no_location_included_group": False
            }
        }
        return default

    def save_settings(self, new_settings=None):
        """Saves the settings to the JSON file, ensuring necessary directories are created."""
        if new_settings:
            self.settings.update(new_settings)

        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir, exist_ok=True)
                self.logger.log_debug(f"Created directory for config file at {config_dir}")
            except OSError as e:
                self.logger.log_error(f"Error creating directory {config_dir}: {e}")
                return

        # Log the settings about to be written for verification
        self.logger.log_debug(f"Saving settings to {self.config_file}: {self.settings}")
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
                self.logger.log_debug(f"Settings successfully saved to {self.config_file}")
        except IOError as e:
            self.logger.log_error(f"Error writing to settings file {self.config_file}: {e}")

    def save_exclusions_partial(self, exclusions):
        """Save only the exclusions part of settings."""
        current_settings = self.load_settings()
        current_settings["exclusions"] = exclusions
        self.save_settings(current_settings)

    def update_exclusions(self, key, item_id, selected):
        """Update a single item in exclusions and save it immediately."""
        exclusions = self.settings.get("exclusions", {})
        if selected:
            if item_id not in exclusions[key]:
                exclusions[key].append(item_id)
        else:
            if item_id in exclusions[key]:
                exclusions[key].remove(item_id)
        
        # Partially save only exclusions
        self.save_exclusions_partial(exclusions)

    def get_window_size_from_settings(self):
        """Fetches the window size from settings or returns default."""
        try:
            window_size = self.settings.get("window_size", {"width": 1000, "height": 600})
            self.logger.log_info(f"Window size retrieved: {window_size}")
            return window_size
        except Exception as e:
            self.logger.log_error(f"Error reading window size from settings: {e}")
            return {"width": 1000, "height": 600}

    def get(self, key, default=None):
        """Gets a setting value by key."""
        value = self.settings.get(key, default)
        self.logger.log_debug(f"Retrieved setting for key '{key}': {value}")
        return value

    def set(self, key, value):
        """Sets a setting value and saves it immediately."""
        self.settings[key] = value
        self.save_settings()
        self.logger.log_debug(f"Set {key} to {value} and saved settings.")

    def reload_settings(self):
        """Reload settings from the JSON file."""
        self.settings = self.load_settings()
        self.logger.log_debug("Settings reloaded.")

    def check_version_file(self):
        """Check if version.txt exists and log an error if it doesn’t."""
        version_file_path = FileHelper.get_version_file_path()
        if not os.path.exists(version_file_path):
            self.logger.log_error("version.txt not found")
        else:
            self.logger.log_info("version.txt found successfully.")
