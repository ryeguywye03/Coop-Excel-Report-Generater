from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QScrollArea, QWidget

class CheckboxManager:
    def __init__(self, layout):
        self.layout = layout
        self.checkboxes = {}

    def populate_checkboxes(self, columns, selected_columns=[]):
        """Populate the layout with checkboxes based on the provided column names."""
        # Clear existing checkboxes
        self.clear_checkboxes()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Add checkboxes for each column
        for column in columns:
            checkbox = QCheckBox(column)
            if column in selected_columns:
                checkbox.setChecked(True)
            scroll_layout.addWidget(checkbox)
            self.checkboxes[column] = checkbox

        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)

    def get_selected_columns(self):
        """Return a list of selected (checked) columns."""
        return [column for column, checkbox in self.checkboxes.items() if checkbox.isChecked()]

    def clear_checkboxes(self):
        """Clear the current checkboxes from the layout."""
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.checkboxes.clear()
