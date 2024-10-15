from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QCompleter
from PyQt5.QtCore import Qt
import json

class SettingsDialog(QDialog):
    def __init__(self, parent, sr_types=None, group_descriptions=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setObjectName("settings_dialog")  # For QSS styling
        self.setFixedSize(400, 300)  # Adjust size if necessary
        
        # Load data (SR types and Group descriptions) - Passed via the JSON later
        self.sr_types = sr_types if sr_types else []
        self.group_descriptions = group_descriptions if group_descriptions else []

        # Create the layout
        layout = QVBoxLayout()

        # SR Type exclusion dropdown
        layout.addWidget(QLabel("Exclude SR Type Description:"))
        self.sr_type_dropdown = QComboBox()
        self.sr_type_dropdown.setEditable(True)
        self.sr_type_dropdown.setCompleter(QCompleter(self.sr_types, self))
        self.sr_type_dropdown.addItems(self.sr_types)
        layout.addWidget(self.sr_type_dropdown)

        # Group Description exclusion dropdown
        layout.addWidget(QLabel("Exclude Group Description:"))
        self.group_dropdown = QComboBox()
        self.group_dropdown.setEditable(True)
        self.group_dropdown.setCompleter(QCompleter(self.group_descriptions, self))
        self.group_dropdown.addItems(self.group_descriptions)
        layout.addWidget(self.group_dropdown)

        # Save button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Set layout
        self.setLayout(layout)

    def save_settings(self):
        """Retrieve the selected values for exclusions."""
        excluded_sr_type = self.sr_type_dropdown.currentText()
        excluded_group = self.group_dropdown.currentText()
        self.exclusions = {
            'excluded_sr_type': excluded_sr_type,
            'excluded_group': excluded_group
        }
        self.accept()

    def get_exclusions(self):
        """Return the selected exclusions."""
        return self.exclusions

