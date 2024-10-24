import json
import os
from utils import resource_path

class SettingsManager:
    def __init__(self):
        self.config_path = resource_path(os.path.join('config', 'settings.json'))

    def load_settings(self):
        """Load settings from a JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                settings = json.load(f)
                settings.setdefault('excluded_sr_type', [])
                settings.setdefault('excluded_group', [])
                settings.setdefault('no_location_excluded_sr_type', [])
                settings.setdefault('no_location_excluded_group', [])
                return settings
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'excluded_sr_type': [],
                'excluded_group': [],
                'no_location_excluded_sr_type': [],
                'no_location_excluded_group': []
            }

    def save_settings(self, settings):
        """Save settings to a JSON file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(settings, f, indent=4)
