import json
import os

class SettingsManager:
    def __init__(self, config_file="settings.json"):
        self.config_file = os.path.join(os.path.dirname(__file__), '..', 'config', config_file)
        self.settings = self.load_settings()

    def load_settings(self):
        """Loads settings from the JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"Error reading {self.config_file}, resetting to default settings.")
                    return self.default_settings()
        else:
            print(f"No settings file found, creating default settings in {self.config_file}.")
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
        self.save_settings(default)
        return default

    def save_settings(self, settings=None):
        """Saves the settings to the JSON file."""
        if settings:
            self.settings = settings
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key, default=None):
        """Gets a setting value by key."""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Sets a setting value."""
        self.settings[key] = value
        self.save_settings()

    def get_exclusions(self):
        """Return the exclusions from settings."""
        return self.settings.get('exclusions', {
            "excluded_sr_type": [],
            "excluded_group": [],
            "no_location_excluded_sr_type": [],
            "no_location_excluded_group": []
        })

    def set_exclusions(self, exclusions):
        """Set the exclusions in settings."""
        self.settings['exclusions'] = exclusions
        self.save_settings()

