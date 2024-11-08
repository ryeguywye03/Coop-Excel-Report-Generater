import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QListWidgetItem, QCheckBox, 
    QLineEdit, QGroupBox, QHBoxLayout, QWidget
)
from PyQt6.QtCore import Qt
from functools import partial
from utils.app_settings import AppSettings  # Use the centralized AppSettings
from utils import LoggerManager  # Ensure LoggerManager is imported

class SettingsDialog(QDialog):
    def __init__(self, parent, sr_types=None, group_descriptions=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setObjectName("settings_dialog")
        self.setMinimumWidth(800)

        # Initialize Logger and AppSettings
        self.logger = LoggerManager(enable_logging=True)
        self.app_settings = AppSettings()
        
        # Retrieve exclusions from settings or set defaults
        self.exclusions = self.app_settings.get('exclusions', {
            'excluded_sr_type': [],
            'excluded_group': [],
            'no_location_excluded_sr_type': [],
            'no_location_excluded_group': [],
            'no_location_included_sr_type': [],
            'no_location_included_group': []
        })

        # Store selections using IDs for each section
        self.temp_selected_excluded_sr_types = {str(id): False for id in sr_types.keys()}
        self.temp_selected_excluded_groups = {str(id): False for id in group_descriptions.keys()}
        self.temp_selected_no_location_excluded_sr_types = {str(id): False for id in sr_types.keys()}
        self.temp_selected_no_location_excluded_groups = {str(id): False for id in group_descriptions.keys()}
        self.temp_selected_no_location_included_sr_types = {str(id): False for id in sr_types.keys()}
        self.temp_selected_no_location_included_groups = {str(id): False for id in group_descriptions.keys()}

        # Load saved selections to the temporary state
        self.load_selected_exclusions()

        # Initialize UI components
        self.setup_ui(sr_types, group_descriptions)

    def load_selected_exclusions(self):
        """Load saved exclusions and store them in the temporary state dictionaries."""
        for item_id in self.exclusions.get('excluded_sr_type', []):
            if item_id in self.temp_selected_excluded_sr_types:
                self.temp_selected_excluded_sr_types[item_id] = True
        for item_id in self.exclusions.get('excluded_group', []):
            if item_id in self.temp_selected_excluded_groups:
                self.temp_selected_excluded_groups[item_id] = True
        for item_id in self.exclusions.get('no_location_excluded_sr_type', []):
            if item_id in self.temp_selected_no_location_excluded_sr_types:
                self.temp_selected_no_location_excluded_sr_types[item_id] = True
        for item_id in self.exclusions.get('no_location_excluded_group', []):
            if item_id in self.temp_selected_no_location_excluded_groups:
                self.temp_selected_no_location_excluded_groups[item_id] = True
        for item_id in self.exclusions.get('no_location_included_sr_type', []):
            if item_id in self.temp_selected_no_location_included_sr_types:
                self.temp_selected_no_location_included_sr_types[item_id] = True
        for item_id in self.exclusions.get('no_location_included_group', []):
            if item_id in self.temp_selected_no_location_included_groups:
                self.temp_selected_no_location_included_groups[item_id] = True

    def setup_ui(self, sr_types, group_descriptions):
        """Initialize the settings UI with exclusion/inclusion lists and search functionality."""
        main_layout = QHBoxLayout(self)

        # Create exclusion card for SR types and groups
        exclude_card = self.create_exclusion_card("Exclude SR Types and Groups",
                                                  sr_types, group_descriptions,
                                                  self.temp_selected_excluded_sr_types, self.temp_selected_excluded_groups)
        main_layout.addWidget(exclude_card)

        # Create No Location Exclusion card with enable toggle
        no_location_exclude_card = self.create_exclusion_card("No Location Exclusion (Exclude SRs with 0,0 coordinates)",
                                                              sr_types, group_descriptions,
                                                              self.temp_selected_no_location_excluded_sr_types, 
                                                              self.temp_selected_no_location_excluded_groups,
                                                              enable_toggle=True)
        main_layout.addWidget(no_location_exclude_card)

        # Create No Location Inclusion card with enable toggle
        no_location_include_card = self.create_exclusion_card("No Location Inclusion (Include SRs with 0,0 coordinates)",
                                                              sr_types, group_descriptions,
                                                              self.temp_selected_no_location_included_sr_types, 
                                                              self.temp_selected_no_location_included_groups,
                                                              enable_toggle=True)
        main_layout.addWidget(no_location_include_card)

        # Buttons for saving and refreshing
        button_layout = QVBoxLayout()
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)

        self.refresh_button = QPushButton("Refresh Descriptions")
        self.refresh_button.clicked.connect(self.refresh_descriptions)
        button_layout.addWidget(self.refresh_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def create_exclusion_card(self, title, sr_types, group_descriptions, selected_sr_dict, selected_group_dict, enable_toggle=False):
        """Helper to create an exclusion/inclusion card with checkboxes, search functionality, and an optional enable toggle."""
        card = QGroupBox(title)
        layout = QVBoxLayout(card)

        # Add an enable checkbox at the top if specified
        if enable_toggle:
            enable_checkbox = QCheckBox(f"Enable {title}")
            enable_checkbox.setChecked(False)  # Default unchecked
            layout.addWidget(enable_checkbox)
            # Connect the toggle to enable or disable the rest of the card's widgets
            enable_checkbox.toggled.connect(lambda checked: self.toggle_card_widgets(card, checked))

        # SR Type section
        layout.addWidget(QLabel("SR Type Description:"))
        sr_type_search = QLineEdit()
        sr_type_search.setPlaceholderText("Search SR Type Description...")
        layout.addWidget(sr_type_search)

        sr_type_list_widget = QListWidget()
        self.populate_list_with_checkboxes(sr_type_list_widget, sr_types, selected_sr_dict, "SR Type")
        layout.addWidget(sr_type_list_widget)

        sr_type_search.textChanged.connect(partial(self.filter_list, sr_type_list_widget, sr_types, selected_sr_dict, "SR Type"))

        # Group section
        layout.addWidget(QLabel("Group Description:"))
        group_search = QLineEdit()
        group_search.setPlaceholderText("Search Group Description...")
        layout.addWidget(group_search)

        group_list_widget = QListWidget()
        self.populate_list_with_checkboxes(group_list_widget, group_descriptions, selected_group_dict, "Group")
        layout.addWidget(group_list_widget)

        group_search.textChanged.connect(partial(self.filter_list, group_list_widget, group_descriptions, selected_group_dict, "Group"))

        return card

    def toggle_card_widgets(self, card, enabled):
        """Enable or disable all widgets within a card."""
        for widget in card.findChildren(QWidget):
            widget.setEnabled(enabled)

    def populate_list_with_checkboxes(self, list_widget, items, selected_dict, item_type="Item"):
        """Populate the list widget with checkboxes, setting their initial state based on selected_dict."""
        list_widget.clear()
        for item_id, item_data in items.items():
            list_item = QListWidgetItem(list_widget)
            checkbox = QCheckBox(item_data["description"])
            checkbox.setChecked(selected_dict.get(item_id, False))

            # Connect state change to update the temporary selection state and save partially
            checkbox.stateChanged.connect(partial(self.update_selected_items, item_id=item_id, selected_dict=selected_dict, description=item_data["description"], item_type=item_type))
            
            list_widget.addItem(list_item)
            list_widget.setItemWidget(list_item, checkbox)

    def update_selected_items(self, state, item_id, selected_dict, description, item_type):
        """Update temporary state based on checkbox interaction, log action, and partially save selection."""
        selected = self.sender().isChecked()  # Use isChecked() to check the checkbox state directly
        selected_dict[item_id] = selected

        # Log the checkbox interaction
        status = "Checked" if selected else "Unchecked"
        self.logger.log_info(f"{item_type} '{description}' ({item_id}) is {status}")

        # Partially save the current selection state to AppSettings
        self.save_partial_settings()

    def save_partial_settings(self):
        """Partially save the current selection states to persist selections even during searches."""
        exclusions = {
            'excluded_sr_type': [item_id for item_id, selected in self.temp_selected_excluded_sr_types.items() if selected],
            'excluded_group': [item_id for item_id, selected in self.temp_selected_excluded_groups.items() if selected],
            'no_location_excluded_sr_type': [item_id for item_id, selected in self.temp_selected_no_location_excluded_sr_types.items() if selected],
            'no_location_excluded_group': [item_id for item_id, selected in self.temp_selected_no_location_excluded_groups.items() if selected],
            'no_location_included_sr_type': [item_id for item_id, selected in self.temp_selected_no_location_included_sr_types.items() if selected],
            'no_location_included_group': [item_id for item_id, selected in self.temp_selected_no_location_included_groups.items() if selected]
        }

        # Update only exclusions in AppSettings without saving other settings
        current_settings = self.app_settings.load_settings()
        current_settings["exclusions"] = exclusions
        self.app_settings.save_settings(current_settings)

    def filter_list(self, list_widget, items, selected_dict, item_type, search_text):
        """Filter the list based on search text and repopulate checkboxes with saved states."""
        filtered_items = {item_id: data for item_id, data in items.items() if search_text.lower() in data["description"].lower()}
        self.populate_list_with_checkboxes(list_widget, filtered_items, selected_dict, item_type)

    def save_settings(self):
        """Save the current state of selections to the settings JSON file through AppSettings."""
        # Prepare the exclusions dictionary based on temporary selections
        self.exclusions = {
            'excluded_sr_type': [item_id for item_id, selected in self.temp_selected_excluded_sr_types.items() if selected],
            'excluded_group': [item_id for item_id, selected in self.temp_selected_excluded_groups.items() if selected],
            'no_location_excluded_sr_type': [item_id for item_id, selected in self.temp_selected_no_location_excluded_sr_types.items() if selected],
            'no_location_excluded_group': [item_id for item_id, selected in self.temp_selected_no_location_excluded_groups.items() if selected],
            'no_location_included_sr_type': [item_id for item_id, selected in self.temp_selected_no_location_included_sr_types.items() if selected],
            'no_location_included_group': [item_id for item_id, selected in self.temp_selected_no_location_included_groups.items() if selected]
        }

        # Load current settings and update exclusions
        current_settings = self.app_settings.load_settings()
        current_settings["exclusions"] = self.exclusions
        self.app_settings.save_settings(current_settings)

        # Close the dialog
        self.accept()

    def get_exclusions(self):
        """Return the current exclusions set in the dialog for use in SettingsHandler."""
        return self.exclusions

    def refresh_descriptions(self):
        """Refresh the SR Type and Group descriptions, updating the lists."""
        # Re-fetch the data if available from the parent or reload source
        if self.parent():
            try:
                self.sr_types = {str(key): val for key, val in self.parent().sr_types.items()}
                self.group_descriptions = {str(key): val for key, val in self.parent().group_descriptions.items()}
            except Exception as e:
                self.sr_types = {}
                self.group_descriptions = {}
                print(f"Error loading SR Types or Group Descriptions: {e}")

        # Repopulate checkboxes with refreshed data and maintain current selection states
        self.populate_list_with_checkboxes(self.sr_type_list, self.sr_types, self.temp_selected_excluded_sr_types, "SR Type")
        self.populate_list_with_checkboxes(self.group_list, self.group_descriptions, self.temp_selected_excluded_groups, "Group")
        self.populate_list_with_checkboxes(self.no_location_sr_type_list, self.sr_types, self.temp_selected_no_location_excluded_sr_types, "SR Type")
        self.populate_list_with_checkboxes(self.no_location_group_list, self.group_descriptions, self.temp_selected_no_location_excluded_groups, "Group")
        self.populate_list_with_checkboxes(self.no_location_included_sr_type_list, self.sr_types, self.temp_selected_no_location_included_sr_types, "SR Type")
        self.populate_list_with_checkboxes(self.no_location_included_group_list, self.group_descriptions, self.temp_selected_no_location_included_groups, "Group")

        # Optionally clear search fields after refreshing
        self.sr_type_search.clear()
        self.group_search.clear()
        self.no_location_sr_type_search.clear()
        self.no_location_group_search.clear()
        self.no_location_included_sr_type_search.clear()
        self.no_location_included_group_search.clear()
