from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox
from utils.app_settings import AppSettings

class SettingsHandler(QDialog):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Main Menu Settings")
        self.setMinimumWidth(200)
        self.setMinimumHeight(150)
        self.main_app = main_app  # Store main_app for access

        # Access the app settings
        self.settings = AppSettings()
        self.changed_settings = []

        # Setup the UI components
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI components for the settings dialog."""
        layout = QVBoxLayout()

        # Theme selection dropdown
        theme_label = QLabel("Select Theme:")
        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(["Light", "Dark"])
        
        # Set current theme based on saved settings
        current_theme = self.settings.get("theme", "dark").capitalize()
        self.theme_dropdown.setCurrentText(current_theme)
        
        # Track change event
        self.theme_dropdown.currentIndexChanged.connect(lambda: self.track_change("theme"))

        # Add components to layout
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_dropdown)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)

        layout.addWidget(save_button)
        self.setLayout(layout)

    def track_change(self, setting_name):
        """Track changed settings by adding them to the changed_settings list."""
        if setting_name not in self.changed_settings:
            self.changed_settings.append(setting_name)

    def save_settings(self):
        """Save the selected theme to the settings."""
        selected_theme = self.theme_dropdown.currentText().lower()  # Lowercase to match QSS filenames
        current_theme = self.settings.get("theme", "dark")

        if current_theme != selected_theme:
            self.settings.set("theme", selected_theme)
            self.main_app.logger.log_info(f"Theme changed to {selected_theme}")
            self.main_app.reload_stylesheet()  # Apply the new theme immediately
        else:
            self.main_app.logger.log_info("Theme not changed; it remains as " + current_theme)

        self.accept()  # Close the dialog after saving
