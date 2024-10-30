from PyQt6.QtWidgets import QCheckBox, QVBoxLayout

class CheckboxManager:
    def __init__(self, layout):
        """Initialize CheckboxManager with the layout where checkboxes will be added."""
        self.layout = layout
        self.checkboxes = []

    def populate_checkboxes(self, column_names):
        """Dynamically create checkboxes for each column name."""
        # Clear any existing checkboxes
        self.clear_checkboxes()

        # Add new checkboxes based on column names
        for col in column_names:
            checkbox = QCheckBox(col)
            self.layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

    def get_selected_columns(self):
        """Returns a list of selected columns based on checked checkboxes."""
        return [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]

    def clear_checkboxes(self):
        """Clear all checkboxes from the layout and reset the list."""
        while self.checkboxes:
            checkbox = self.checkboxes.pop()
            self.layout.removeWidget(checkbox)
            checkbox.deleteLater()
