# settings_handler.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox
from modules.utils import AppSettings
from modules.dialogs.editable_table_dialog import EditableTableDialog

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

        # Buttons to open editable table dialogs for Types and Groups
        edit_types_button = QPushButton("Edit Types")
        edit_types_button.clicked.connect(self.open_types_dialog)
        edit_groups_button = QPushButton("Edit Groups")
        edit_groups_button.clicked.connect(self.open_groups_dialog)

        layout.addWidget(edit_types_button)
        layout.addWidget(edit_groups_button)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def open_types_dialog(self):
        # Open dialog for editing Types using "311_GIS_Type_Descriptions.xlsx" file
        dialog = EditableTableDialog(["Type"], "311_GIS_Type_Descriptions.xlsx", self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass  # Post-editing logic for types can go here if needed

    def open_groups_dialog(self):
        # Open dialog for editing Groups using "311_GIS_Group_Descriptions.xlsx" file
        dialog = EditableTableDialog(["Group"], "311_GIS_Group_Descriptions.xlsx", self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass  # Post-editing logic for groups can go here if needed

    def track_change(self, setting_name):
        """Track changed settings by adding them to the changed_settings list."""
        if setting_name not in self.changed_settings:
            self.changed_settings.append(setting_name)

    def save_settings(self):
        """Save the selected theme to the settings."""
        selected_theme = self.theme_dropdown.currentText().lower()  # Lowercase to match QSS filenames
        current_theme = self.settings.get("theme", "dark")

        if current_theme != selected_theme:
            new_theme = "dark" if current_theme == "light" else "light"
            self.main_app.settings.set("theme", new_theme)
            self.main_app.apply_stylesheet(force=True)
            self.main_app.logger.log_info(f"Theme changed to {new_theme}")
        else:
            self.main_app.logger.log_info("Theme not changed; it remains as " + current_theme)

        self.accept()  # Close the dialog after saving
