import json
import os
import sys
from utils import LoggerManager, FileHelper  # Ensure LoggerManager and resource_path are imported

class AppSettings:
    def __init__(self, config_filename="settings.json"):
        # Initialize logger
        self.logger = LoggerManager()

        # Set the config directory and file path using FileHelper
        self.config_dir = FileHelper.resource_path('config')  # Use resource_path to locate the config directory
        self.config_file = FileHelper.get_settings_file_path()  # Use FileHelper to get the settings file path

        # Ensure the config directory and file are ready
        self.prepare_config_file()

        # Load settings or initialize defaults
        self.settings = self.load_settings()

    def prepare_config_file(self):
        """Ensures that the config directory and settings file exist."""
        if not os.path.exists(self.config_dir):
            try:
                os.makedirs(self.config_dir)
                self.logger.log_debug(f"Created config directory at {self.config_dir}")
            except OSError as e:
                self.logger.log_error(f"Failed to create config directory {self.config_dir}: {e}")

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
            except json.JSONDecodeError:
                self.logger.log_error(f"JSON decode error in {self.config_file}. Reverting to default settings.")
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
                "no_location_excluded_group": []
            }
        }
        return default

    def save_settings(self, new_settings=None):
        """Saves the settings to the JSON file, ensuring necessary directories are created."""
        if new_settings:
            self.settings.update(new_settings)

        if not os.path.exists(self.config_dir):
            try:
                os.makedirs(self.config_dir, exist_ok=True)
                self.logger.log_debug(f"Created directory for config file at {self.config_dir}")
            except OSError as e:
                self.logger.log_error(f"Error creating directory {self.config_dir}: {e}")
                return

        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
                self.logger.log_debug(f"Settings saved to {self.config_file}")
        except IOError as e:
            self.logger.log_error(f"Error writing to settings file {self.config_file}: {e}")

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
        return self.settings.get(key, default)

    def set(self, key, value):
        """Sets a setting value and saves it immediately."""
        self.settings[key] = value
        self.save_settings()
        self.logger.log_debug(f"Set {key} to {value} and saved settings.")

    def reload_settings(self):
        """Reload settings from the JSON file."""
        self.settings = self.load_settings()
