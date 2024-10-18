from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QListWidgetItem, QCheckBox, QLineEdit, QGroupBox, QHBoxLayout, QScrollArea, QWidget
from PyQt5.QtCore import Qt
import json
import os

class SettingsDialog(QDialog):
    def __init__(self, parent, sr_types=None, group_descriptions=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setObjectName("settings_dialog")
        self.setMinimumWidth(800)

        # Initialize exclusions attribute
        self.exclusions = {
            'excluded_sr_types': [],
            'excluded_groups': [],
            'no_location_excluded_sr_types': [],
            'no_location_excluded_groups': []
        }

        # Setup the types and groups data
        self.sr_types = [sr["description"] for sr in sr_types.values()] if sr_types else []
        self.group_descriptions = [group["description"] for group in group_descriptions.values()] if group_descriptions else []

        # Load saved exclusions from the JSON file
        self.config_path = os.path.join(os.path.dirname(__file__), '../config/settings.json')
        self.saved_exclusions = self.load_saved_exclusions()

        # Initialize the UI
        self.setup_ui()

    def load_saved_exclusions(self):
        """Load saved exclusions from the settings.json file."""
        try:
            with open(self.config_path, 'r') as f:
                exclusions = json.load(f)
                exclusions.setdefault('no_location_excluded_sr_types', [])
                exclusions.setdefault('no_location_excluded_groups', [])
                return exclusions
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'excluded_sr_types': [],
                'excluded_groups': [],
                'no_location_excluded_sr_types': [],
                'no_location_excluded_groups': []
            }

    def load_saved_exclusions(self):
        """Load saved exclusions from the settings.json file."""
        try:
            with open(self.config_path, 'r') as f:
                exclusions = json.load(f)
                # Add default values if keys are missing
                exclusions.setdefault('no_location_excluded_sr_types', [])
                exclusions.setdefault('no_location_excluded_groups', [])
                return exclusions
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'excluded_sr_types': [],
                'excluded_groups': [],
                'no_location_excluded_sr_types': [],
                'no_location_excluded_groups': []
            }

    def setup_ui(self):
        """Initialize the settings UI."""
        main_layout = QHBoxLayout(self)  # Create the horizontal layout for side-by-side cards

        # Create a card for Exclude SR Type and Group section
        exclude_card = QGroupBox("Exclude SR Types and Groups")
        exclude_layout = QVBoxLayout(exclude_card)

        # Exclude SR Type section
        exclude_layout.addWidget(QLabel("Exclude SR Type Description:"))
        self.sr_type_search = QLineEdit(self)
        self.sr_type_search.setPlaceholderText("Search SR Type Description...")
        self.sr_type_search.textChanged.connect(lambda: self.filter_list(self.sr_type_list, self.sr_types, self.sr_type_search.text()))  # Connect the search functionality
        exclude_layout.addWidget(self.sr_type_search)
        self.sr_type_list = QListWidget()
        self.populate_list_with_checkboxes(self.sr_type_list, self.sr_types, self.saved_exclusions['excluded_sr_types'])
        exclude_layout.addWidget(self.sr_type_list)

        # Exclude Group Description section
        exclude_layout.addWidget(QLabel("Exclude Group Description:"))
        self.group_search = QLineEdit(self)
        self.group_search.setPlaceholderText("Search Group Description...")
        self.group_search.textChanged.connect(lambda: self.filter_list(self.group_list, self.group_descriptions, self.group_search.text()))  # Connect the search functionality
        exclude_layout.addWidget(self.group_search)
        self.group_list = QListWidget()
        self.populate_list_with_checkboxes(self.group_list, self.group_descriptions, self.saved_exclusions['excluded_groups'])
        exclude_layout.addWidget(self.group_list)

        # Create the scrollable section for No Location Exclusion
        self.no_location_card = QGroupBox("No Location Exclusion (Exclude SRs with 0,0 coordinates)")
        no_location_layout = QVBoxLayout(self.no_location_card)

        # Add the Enable No Location Exclusion checkbox inside the No Location card
        self.no_location_enabled_checkbox = QCheckBox("Enable No Location Exclusion")
        self.no_location_enabled_checkbox.setChecked(False)
        self.no_location_enabled_checkbox.toggled.connect(self.toggle_no_location_exclusion)
        no_location_layout.addWidget(self.no_location_enabled_checkbox)

        # No Location Exclusion SR Type section
        no_location_layout.addWidget(QLabel("Exclude SR Type Description (No Location):"))
        self.no_location_sr_type_search = QLineEdit(self)
        self.no_location_sr_type_search.setPlaceholderText("Search SR Type Description (No Location)...")
        self.no_location_sr_type_search.textChanged.connect(lambda: self.filter_list(self.no_location_sr_type_list, self.sr_types, self.no_location_sr_type_search.text()))  # Connect the search functionality
        no_location_layout.addWidget(self.no_location_sr_type_search)
        self.no_location_sr_type_list = QListWidget()
        self.populate_list_with_checkboxes(
            self.no_location_sr_type_list,
            self.sr_types,
            self.saved_exclusions['no_location_excluded_sr_types']
        )
        no_location_layout.addWidget(self.no_location_sr_type_list)

        # No Location Exclusion Group section
        no_location_layout.addWidget(QLabel("Exclude Group Description (No Location):"))
        self.no_location_group_search = QLineEdit(self)
        self.no_location_group_search.setPlaceholderText("Search Group Description (No Location)...")
        self.no_location_group_search.textChanged.connect(lambda: self.filter_list(self.no_location_group_list, self.group_descriptions, self.no_location_group_search.text()))  # Connect the search functionality
        no_location_layout.addWidget(self.no_location_group_search)
        self.no_location_group_list = QListWidget()
        self.populate_list_with_checkboxes(
            self.no_location_group_list,
            self.group_descriptions,
            self.saved_exclusions['no_location_excluded_groups']
        )
        no_location_layout.addWidget(self.no_location_group_list)

        # Add both cards side by side in the main layout
        main_layout.addWidget(exclude_card)
        main_layout.addWidget(self.no_location_card)

        # Save and Refresh buttons (placed below the main content)
        button_layout = QVBoxLayout()  # Add buttons at the bottom
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)

        self.refresh_button = QPushButton("Refresh Descriptions")
        self.refresh_button.clicked.connect(self.refresh_descriptions)
        button_layout.addWidget(self.refresh_button)

        main_layout.addLayout(button_layout)  # Add the button layout to the main layout

        self.setLayout(main_layout)

    def toggle_no_location_exclusion(self, checked):
        """Enable or disable the No Location Exclusion section based on the checkbox."""
        self.no_location_card.setEnabled(checked)

    def get_exclusions(self):
        """Return the current exclusions."""
        return self.exclusions

    def populate_list_with_checkboxes(self, list_widget, items, selected_items=[]):
        """Populate a QListWidget with items and preselect checkboxes based on exclusions."""
        list_widget.clear()
        for item in items:
            list_item = QListWidgetItem(list_widget)
            checkbox = QCheckBox(item)
            if item in selected_items:
                checkbox.setChecked(True)  # Pre-check the box if it was excluded
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
        """Retrieve the selected values for exclusions and save them."""
        excluded_sr_types = self.get_selected_items(self.sr_type_list)
        excluded_groups = self.get_selected_items(self.group_list)

        # No Location exclusions
        no_location_excluded_sr_types = self.get_selected_items(self.no_location_sr_type_list)
        no_location_excluded_groups = self.get_selected_items(self.no_location_group_list)

        self.exclusions = {
            'excluded_sr_types': excluded_sr_types,
            'excluded_groups': excluded_groups,
            'no_location_excluded_sr_types': no_location_excluded_sr_types if self.no_location_enabled_checkbox.isChecked() else [],
            'no_location_excluded_groups': no_location_excluded_groups if self.no_location_enabled_checkbox.isChecked() else []
        }

        # Ensure the path to the config directory exists
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        # Save the exclusions to the JSON file in the /config directory
        with open(self.config_path, 'w') as f:
            json.dump(self.exclusions, f, indent=4)

        self.accept()  # Close the dialog after saving

    def filter_list(self, list_widget, items, search_text):
        """Filter the items in the list based on the search text."""
        filtered_items = [item for item in items if search_text.lower() in item.lower()]
        # Repopulate the list with filtered items
        self.populate_list_with_checkboxes(list_widget, filtered_items)

    def refresh_descriptions(self):
        """Refresh the descriptions by reloading the data and repopulating the lists."""
        # Reload the data from the parent (or from an external source if needed)
        if self.parent():
            try:

                self.sr_types = [sr["description"] for sr in self.parent().sr_types.values()]
            except Exception as e:
                self.sr_types = []
                print(f"Error loading SR Types: {e}")
                
            try:
                self.group_descriptions = [group["description"] for group in self.parent().group_descriptions.values()]
            except Exception as e:
                self.group_descriptions = []
                print(f"Error loading Group Descriptions: {e}")

        # Repopulate the lists with the refreshed data
        self.populate_list_with_checkboxes(self.sr_type_list, self.sr_types, self.saved_exclusions['excluded_sr_types'])
        self.populate_list_with_checkboxes(self.group_list, self.group_descriptions, self.saved_exclusions['excluded_groups'])

        # Refresh the no-location exclusion lists as well
        self.populate_list_with_checkboxes(self.no_location_sr_type_list, self.sr_types, self.saved_exclusions['no_location_excluded_sr_types'])
        self.populate_list_with_checkboxes(self.no_location_group_list, self.group_descriptions, self.saved_exclusions['no_location_excluded_groups'])

        # Optionally, reset the search fields after refresh
        self.sr_type_search.clear()
        self.group_search.clear()
        self.no_location_sr_type_search.clear()
        self.no_location_group_search.clear()

    def keyPressEvent(self, event):
        """Handle key press events for the search functionality."""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Trigger search on Enter key press
            self.perform_search()

    def perform_search(self):
        """Filter lists based on the current search fields."""
        sr_type_search_text = self.sr_type_search.text()
        group_search_text = self.group_search.text()
        no_location_sr_type_search_text = self.no_location_sr_type_search.text()
        no_location_group_search_text = self.no_location_group_search.text()

        # Filter the lists based on the search text
        self.filter_list(self.sr_type_list, self.sr_types, sr_type_search_text)
        self.filter_list(self.group_list, self.group_descriptions, group_search_text)
        self.filter_list(self.no_location_sr_type_list, self.sr_types, no_location_sr_type_search_text)
        self.filter_list(self.no_location_group_list, self.group_descriptions, no_location_group_search_text)

