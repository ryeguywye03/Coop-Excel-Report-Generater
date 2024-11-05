import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QListWidgetItem, QCheckBox, 
    QLineEdit, QGroupBox, QHBoxLayout, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt
from utils.app_settings import AppSettings  # Use the centralized AppSettings

class SettingsDialog(QDialog):
    def __init__(self, parent, sr_types=None, group_descriptions=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setObjectName("settings_dialog")
        self.setMinimumWidth(800)

        # Use centralized AppSettings for exclusions and config path
        self.app_settings = AppSettings()
        self.exclusions = self.app_settings.get('exclusions', {
            'excluded_sr_type': [],
            'excluded_group': [],
            'no_location_excluded_sr_type': [],
            'no_location_excluded_group': [],
            'no_location_included_sr_type': [],
            'no_location_included_group': []
        })

        # Setup types and groups data
        self.sr_types = [sr["description"] for sr in sr_types.values()] if sr_types else []
        self.group_descriptions = [group["description"] for group in group_descriptions.values()] if group_descriptions else []

        # Load the saved exclusions from AppSettings
        self.saved_exclusions = self.exclusions

        # Initialize the UI
        self.setup_ui()

    def setup_ui(self):
        """Initialize the settings UI."""
        main_layout = QHBoxLayout(self)

        exclude_card = QGroupBox("Exclude SR Types and Groups")
        exclude_card.setObjectName("excludeCard")  # Add ID for styling
        exclude_layout = QVBoxLayout(exclude_card)

        exclude_layout.addWidget(QLabel("Exclude SR Type Description:"))
        self.sr_type_search = QLineEdit(self)
        self.sr_type_search.setObjectName("srTypeSearch")  # Add ID for styling
        self.sr_type_search.setPlaceholderText("Search SR Type Description...")
        self.sr_type_search.textChanged.connect(lambda: self.filter_list(self.sr_type_list, self.sr_types, self.sr_type_search.text()))
        exclude_layout.addWidget(self.sr_type_search)
        
        self.sr_type_list = QListWidget()
        self.sr_type_list.setObjectName("srTypeList")  # Add ID for styling
        self.populate_list_with_checkboxes(self.sr_type_list, self.sr_types, self.saved_exclusions['excluded_sr_type'])
        exclude_layout.addWidget(self.sr_type_list)

        exclude_layout.addWidget(QLabel("Exclude Group Description:"))
        self.group_search = QLineEdit(self)
        self.group_search.setObjectName("groupSearch")  # Add ID for styling
        self.group_search.setPlaceholderText("Search Group Description...")
        self.group_search.textChanged.connect(lambda: self.filter_list(self.group_list, self.group_descriptions, self.group_search.text()))
        exclude_layout.addWidget(self.group_search)
        
        self.group_list = QListWidget()
        self.group_list.setObjectName("groupList")  # Add ID for styling
        self.populate_list_with_checkboxes(self.group_list, self.group_descriptions, self.saved_exclusions['excluded_group'])
        exclude_layout.addWidget(self.group_list)

        main_layout.addWidget(exclude_card)

        no_location_card = QGroupBox("No Location Exclusion (Exclude SRs with 0,0 coordinates)")
        no_location_card.setObjectName("noLocationCard")  # Add ID for styling
        no_location_layout = QVBoxLayout(no_location_card)

        self.no_location_enabled_checkbox = QCheckBox("Enable No Location Exclusion")
        self.no_location_enabled_checkbox.setChecked(False)
        self.no_location_enabled_checkbox.toggled.connect(self.toggle_no_location_exclusion)
        no_location_layout.addWidget(self.no_location_enabled_checkbox)

        no_location_layout.addWidget(QLabel("Exclude SR Type Description (No Location):"))
        self.no_location_sr_type_search = QLineEdit(self)
        self.no_location_sr_type_search.setObjectName("noLocationSrTypeSearch")  # Add ID for styling
        self.no_location_sr_type_search.setPlaceholderText("Search SR Type Description (No Location)...")
        self.no_location_sr_type_search.textChanged.connect(lambda: self.filter_list(self.no_location_sr_type_list, self.sr_types, self.no_location_sr_type_search.text()))
        no_location_layout.addWidget(self.no_location_sr_type_search)
        
        self.no_location_sr_type_list = QListWidget()
        self.no_location_sr_type_list.setObjectName("noLocationSrTypeList")  # Add ID for styling
        self.populate_list_with_checkboxes(self.no_location_sr_type_list, self.sr_types, self.saved_exclusions['no_location_excluded_sr_type'])
        no_location_layout.addWidget(self.no_location_sr_type_list)

        no_location_layout.addWidget(QLabel("Exclude Group Description (No Location):"))
        self.no_location_group_search = QLineEdit(self)
        self.no_location_group_search.setObjectName("noLocationGroupSearch")  # Add ID for styling
        self.no_location_group_search.setPlaceholderText("Search Group Description (No Location)...")
        self.no_location_group_search.textChanged.connect(lambda: self.filter_list(self.no_location_group_list, self.group_descriptions, self.no_location_group_search.text()))
        no_location_layout.addWidget(self.no_location_group_search)
        
        self.no_location_group_list = QListWidget()
        self.no_location_group_list.setObjectName("noLocationGroupList")  # Add ID for styling
        self.populate_list_with_checkboxes(self.no_location_group_list, self.group_descriptions, self.saved_exclusions['no_location_excluded_group'])
        no_location_layout.addWidget(self.no_location_group_list)

        main_layout.addWidget(no_location_card)

        # New Section for No Location Inclusion
        inclusion_card = QGroupBox("No Location Inclusion (Include SRs with 0,0 coordinates)")
        inclusion_card.setObjectName("inclusionCard")  # Add ID for styling
        inclusion_layout = QVBoxLayout(inclusion_card)

        self.no_location_included_checkbox = QCheckBox("Enable No Location Inclusion")
        self.no_location_included_checkbox.setChecked(False)
        self.no_location_included_checkbox.toggled.connect(self.toggle_no_location_inclusion)
        inclusion_layout.addWidget(self.no_location_included_checkbox)

        # Include SR Type Section
        inclusion_layout.addWidget(QLabel("Include SR Type Description (No Location):"))
        self.no_location_included_sr_type_search = QLineEdit(self)
        self.no_location_included_sr_type_search.setObjectName("noLocationIncludedSrTypeSearch")  # Add ID for styling
        self.no_location_included_sr_type_search.setPlaceholderText("Search SR Type Description (Include No Location)...")
        self.no_location_included_sr_type_search.textChanged.connect(
            lambda: self.filter_list(self.no_location_included_sr_type_list, self.sr_types, self.no_location_included_sr_type_search.text())
        )
        inclusion_layout.addWidget(self.no_location_included_sr_type_search)

        self.no_location_included_sr_type_list = QListWidget()
        self.no_location_included_sr_type_list.setObjectName("noLocationIncludedSrTypeList")  # Add ID for styling
        self.populate_list_with_checkboxes(self.no_location_included_sr_type_list, self.sr_types, self.saved_exclusions['no_location_included_sr_type'])
        inclusion_layout.addWidget(self.no_location_included_sr_type_list)

        # Include Group Section
        inclusion_layout.addWidget(QLabel("Include Group Description (No Location):"))
        self.no_location_included_group_search = QLineEdit(self)
        self.no_location_included_group_search.setObjectName("noLocationIncludedGroupSearch")  # Add ID for styling
        self.no_location_included_group_search.setPlaceholderText("Search Group Description (Include No Location)...")
        self.no_location_included_group_search.textChanged.connect(
            lambda: self.filter_list(self.no_location_included_group_list, self.group_descriptions, self.no_location_included_group_search.text())
        )
        inclusion_layout.addWidget(self.no_location_included_group_search)

        self.no_location_included_group_list = QListWidget()
        self.no_location_included_group_list.setObjectName("noLocationIncludedGroupList")  # Add ID for styling
        self.populate_list_with_checkboxes(self.no_location_included_group_list, self.group_descriptions, self.saved_exclusions['no_location_included_group'])
        inclusion_layout.addWidget(self.no_location_included_group_list)

        # Add the inclusion card to the main layout
        main_layout.addWidget(inclusion_card)

        button_layout = QVBoxLayout()
        self.save_button = QPushButton("Save Settings")
        self.save_button.setObjectName("saveButton")  # Add ID for styling
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)

        self.refresh_button = QPushButton("Refresh Descriptions")
        self.refresh_button.setObjectName("refreshButton")  # Add ID for styling
        self.refresh_button.clicked.connect(self.refresh_descriptions)
        button_layout.addWidget(self.refresh_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def toggle_no_location_exclusion(self, checked):
        self.no_location_sr_type_search.setEnabled(checked)
        self.no_location_group_search.setEnabled(checked)
        self.no_location_sr_type_list.setEnabled(checked)
        self.no_location_group_list.setEnabled(checked)

    def toggle_no_location_inclusion(self, checked):
        self.no_location_included_sr_type_search.setEnabled(checked)
        self.no_location_included_group_search.setEnabled(checked)
        self.no_location_included_sr_type_list.setEnabled(checked)
        self.no_location_included_group_list.setEnabled(checked)

    def save_settings(self):
        """Saves the exclusions settings to the JSON file through AppSettings."""
        self.exclusions = {
            'excluded_sr_type': self.get_selected_items(self.sr_type_list),
            'excluded_group': self.get_selected_items(self.group_list),
            'no_location_excluded_sr_type': self.get_selected_items(self.no_location_sr_type_list) if self.no_location_enabled_checkbox.isChecked() else [],
            'no_location_excluded_group': self.get_selected_items(self.no_location_group_list) if self.no_location_enabled_checkbox.isChecked() else [],
            'no_location_included_sr_type': self.get_selected_items(self.no_location_included_sr_type_list) if self.no_location_included_checkbox.isChecked() else [],
            'no_location_included_group': self.get_selected_items(self.no_location_included_group_list) if self.no_location_included_checkbox.isChecked() else []
        }

        # Update settings globally through AppSettings
        self.app_settings.save_settings({"exclusions": self.exclusions})

        # Close dialog after saving
        self.accept()

    def get_exclusions(self):
        """Return the current exclusion settings."""
        return self.exclusions

    def populate_list_with_checkboxes(self, list_widget, items, selected_items=[]):
        list_widget.clear()
        for item in items:
            list_item = QListWidgetItem(list_widget)
            checkbox = QCheckBox(item)
            if item in selected_items:
                checkbox.setChecked(True)
            list_widget.addItem(list_item)
            list_widget.setItemWidget(list_item, checkbox)

    def get_selected_items(self, list_widget):
        selected_items = []
        for i in range(list_widget.count()):
            item_widget = list_widget.itemWidget(list_widget.item(i))
            if item_widget and item_widget.isChecked():
                selected_items.append(item_widget.text())
        return selected_items

    def filter_list(self, list_widget, items, search_text):
        filtered_items = [item for item in items if search_text.lower() in item.lower()]
        self.populate_list_with_checkboxes(list_widget, filtered_items)

    def refresh_descriptions(self):
        """Refresh the descriptions by reloading the data and repopulating the lists."""
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

        self.populate_list_with_checkboxes(self.sr_type_list, self.sr_types, self.saved_exclusions['excluded_sr_type'])
        self.populate_list_with_checkboxes(self.group_list, self.group_descriptions, self.saved_exclusions['excluded_group'])
        self.populate_list_with_checkboxes(self.no_location_sr_type_list, self.sr_types, self.saved_exclusions['no_location_excluded_sr_type'])
        self.populate_list_with_checkboxes(self.no_location_group_list, self.group_descriptions, self.saved_exclusions['no_location_excluded_group'])
        self.populate_list_with_checkboxes(self.no_location_included_sr_type_list, self.sr_types, self.saved_exclusions['no_location_included_sr_type'])
        self.populate_list_with_checkboxes(self.no_location_included_group_list, self.group_descriptions, self.saved_exclusions['no_location_included_group'])
        
        # Optionally reset the search fields after refresh
        self.sr_type_search.clear()
        self.group_search.clear()
        self.no_location_sr_type_search.clear()
        self.no_location_group_search.clear()
        self.no_location_included_sr_type_search.clear()
        self.no_location_included_group_search.clear()
