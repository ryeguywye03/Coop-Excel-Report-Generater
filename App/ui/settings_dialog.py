from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()

        # No location inclusion criteria
        self.no_location_label = QLabel("Enter SR descriptions to include if X,Y = 0,0:")
        self.no_location_input = QLineEdit()
        layout.addWidget(self.no_location_label)
        layout.addWidget(self.no_location_input)

        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def get_no_location_inclusion(self):
        return self.no_location_input.text()
    

    def sr_count_settings(self):
        """Open the settings dialog to get user preferences."""
        dialog = SettingsDialog(self)
        if dialog.exec_():
            return dialog.get_no_location_inclusion()
        return None
