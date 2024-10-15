from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QListWidgetItem, QCheckBox, QLineEdit
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent, sr_types=None, group_descriptions=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setObjectName("settings_dialog")
        
        # Make the dialog size dynamic
        self.setMinimumWidth(400)

        # Setup the types and groups data
        self.sr_types = [sr["description"] for sr in sr_types.values()] if sr_types else []
        self.group_descriptions = [group["description"] for group in group_descriptions.values()] if group_descriptions else []

        # Initialize the UI
        self.setup_ui()

    def setup_ui(self):
        """Initialize the settings UI."""
        layout = QVBoxLayout(self)

        # SR Type exclusion list with checkboxes
        layout.addWidget(QLabel("Exclude SR Type Description:"))
        self.sr_type_search = QLineEdit(self)
        self.sr_type_search.setPlaceholderText("Search SR Type Description...")
        layout.addWidget(self.sr_type_search)
        self.sr_type_list = QListWidget()
        self.populate_list_with_checkboxes(self.sr_type_list, self.sr_types)
        layout.addWidget(self.sr_type_list)

        # Group Description exclusion list with checkboxes
        layout.addWidget(QLabel("Exclude Group Description:"))
        self.group_search = QLineEdit(self)
        self.group_search.setPlaceholderText("Search Group Description...")
        layout.addWidget(self.group_search)
        self.group_list = QListWidget()
        self.populate_list_with_checkboxes(self.group_list, self.group_descriptions)
        layout.addWidget(self.group_list)

        # Connect the search fields to filter functionality
        self.sr_type_search.textChanged.connect(lambda text: self.filter_list(self.sr_type_list, self.sr_types, text))
        self.group_search.textChanged.connect(lambda text: self.filter_list(self.group_list, self.group_descriptions, text))

        # Save and Refresh buttons
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.refresh_button = QPushButton("Refresh Descriptions")
        self.refresh_button.clicked.connect(self.refresh_descriptions)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

    def populate_list_with_checkboxes(self, list_widget, items):
        """Populate a QListWidget with items and checkboxes."""
        list_widget.clear()
        for item in items:
            list_item = QListWidgetItem(list_widget)
            checkbox = QCheckBox(item)
            list_widget.addItem(list_item)
            list_widget.setItemWidget(list_item, checkbox)

    def get_selected_items(self, list_widget):
        """Get the checked items from a QListWidget."""
        selected_items = []
        for i in range(list_widget.count()):
            item_widget = list_widget.itemWidget(list_widget.item(i))
            if item_widget and item_widget.isChecked():
                selected_items.append(item_widget.text())
        return selected_items

    def save_settings(self):
        """Retrieve the selected values for exclusions."""
        excluded_sr_types = self.get_selected_items(self.sr_type_list)
        excluded_groups = self.get_selected_items(self.group_list)
        self.exclusions = {
            'excluded_sr_types': excluded_sr_types,
            'excluded_groups': excluded_groups
        }
        self.accept()

    def filter_list(self, list_widget, items, search_text):
        """Filter the items in the list based on the search text."""
        filtered_items = [item for item in items if search_text.lower() in item.lower()]
        self.populate_list_with_checkboxes(list_widget, filtered_items)


    def refresh_descriptions(self):
        """Refresh the descriptions based on the Excel files."""
        settings_manager = self.parent().settings_manager
        settings_manager.create_json_from_excel()

        # Reload the settings after refreshing the Excel data
        self.sr_type_list.clear()
        self.group_list.clear()

        # Reload SR Types and Group Descriptions
        self.sr_types = [sr["description"] for sr in settings_manager.load_settings().get("type_descriptions", {}).values()]
        self.group_descriptions = [group["description"] for group in settings_manager.load_settings().get("group_descriptions", {}).values()]

        # Repopulate the lists
        self.populate_list(self.sr_type_list, self.sr_types)
        self.populate_list(self.group_list, self.group_descriptions)
