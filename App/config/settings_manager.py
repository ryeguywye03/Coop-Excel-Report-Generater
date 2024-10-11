class SettingsManager:
    def __init__(self):
        self.no_location_inclusion = ""

    def save_settings(self, descriptions):
        """Save the no location inclusion descriptions."""
        self.no_location_inclusion = descriptions

    def load_settings(self):
        """Return the saved no location inclusion descriptions."""
        return self.no_location_inclusion
