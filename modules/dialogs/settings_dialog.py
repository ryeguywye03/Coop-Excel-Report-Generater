import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QListWidgetItem, QCheckBox,
    QLineEdit, QGroupBox, QHBoxLayout, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from functools import partial
from modules.utils.app_settings import AppSettings
from modules.utils import LoggerManager  # Ensure LoggerManager is imported
from modules.utils.file_helpers import FileHelper  # Assuming this helper class is used to handle file paths

class SettingsDialog(QDialog):
    def __init__(self, parent, sr_types=None, group_descriptions=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setObjectName("settings_dialog")
        self.setMinimumWidth(800)

        # Initialize Logger and AppSettings
        self.logger = LoggerManager(enable_logging=True)
        self.app_settings = AppSettings()

        # Set default data structures if None
        self.sr_types = sr_types if sr_types is not None else {}
        self.group_descriptions = group_descriptions if group_descriptions is not None else {}

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
        self.temp_selected_excluded_sr_types = {str(id): False for id in self.sr_types.keys()}
        self.temp_selected_excluded_groups = {str(id): False for id in self.group_descriptions.keys()}
        self.temp_selected_no_location_excluded_sr_types = {str(id): False for id in self.sr_types.keys()}
        self.temp_selected_no_location_excluded_groups = {str(id): False for id in self.group_descriptions.keys()}
        self.temp_selected_no_location_included_sr_types = {str(id): False for id in self.sr_types.keys()}
        self.temp_selected_no_location_included_groups = {str(id): False for id in self.group_descriptions.keys()}

        # Load saved selections to the temporary state
        self.load_selected_exclusions()

        # Initialize UI components
        self.setup_ui(self.sr_types, self.group_descriptions)

    def load_selected_exclusions(self):
        """Load saved exclusions and store them in the temporary state dictionaries."""
        if not isinstance(self.exclusions, dict):
            self.logger.log_error("Exclusions data is not a dictionary. Using an empty dictionary as a fallback.")
            exclusions = {}
        else:
            exclusions = self.exclusions

        for key in ['excluded_sr_type', 'excluded_group', 'no_location_excluded_sr_type', 
                    'no_location_excluded_group', 'no_location_included_sr_type', 'no_location_included_group']:
            if not isinstance(exclusions.get(key, []), list):
                self.logger.log_error(f"Exclusion key '{key}' is not a list in the JSON data. Defaulting to an empty list.")
                exclusions[key] = []  # Set it to an empty list if it’s not a list

        # Load each exclusion into the temporary selection dictionaries
        for item_id in exclusions.get('excluded_sr_type', []):
            if item_id in self.temp_selected_excluded_sr_types:
                self.temp_selected_excluded_sr_types[item_id] = True

        for item_id in exclusions.get('excluded_group', []):
            if item_id in self.temp_selected_excluded_groups:
                self.temp_selected_excluded_groups[item_id] = True

        for item_id in exclusions.get('no_location_excluded_sr_type', []):
            if item_id in self.temp_selected_no_location_excluded_sr_types:
                self.temp_selected_no_location_excluded_sr_types[item_id] = True

        for item_id in exclusions.get('no_location_excluded_group', []):
            if item_id in self.temp_selected_no_location_excluded_groups:
                self.temp_selected_no_location_excluded_groups[item_id] = True

        for item_id in exclusions.get('no_location_included_sr_type', []):
            if item_id in self.temp_selected_no_location_included_sr_types:
                self.temp_selected_no_location_included_sr_types[item_id] = True

        for item_id in exclusions.get('no_location_included_group', []):
            if item_id in self.temp_selected_no_location_included_groups:
                self.temp_selected_no_location_included_groups[item_id] = True

    def setup_ui(self, sr_types, group_descriptions):
        """Initialize the settings UI with exclusion/inclusion lists and search functionality."""
        main_layout = QHBoxLayout(self)

        # Use saved settings to set the enable checkboxes correctly
        self.exclude_enable_checkbox = None
        if "enable_excluded" in self.exclusions:
            exclude_card, self.exclude_enable_checkbox = self.create_exclusion_card(
                "Exclude SR Types and Groups", sr_types, group_descriptions,
                self.temp_selected_excluded_sr_types, self.temp_selected_excluded_groups,
                enable_toggle=True
            )
            self.exclude_enable_checkbox.setChecked(self.exclusions["enable_excluded"])  # Load saved state
        main_layout.addWidget(exclude_card)

        self.no_location_exclude_enable_checkbox = None
        if "enable_no_location_excluded" in self.exclusions:
            no_location_exclude_card, self.no_location_exclude_enable_checkbox = self.create_exclusion_card(
                "No Location Exclusion (Exclude SRs with 0,0 coordinates)", sr_types, group_descriptions,
                self.temp_selected_no_location_excluded_sr_types, self.temp_selected_no_location_excluded_groups,
                enable_toggle=True
            )
            self.no_location_exclude_enable_checkbox.setChecked(self.exclusions["enable_no_location_excluded"])  # Load saved state
        main_layout.addWidget(no_location_exclude_card)

        self.no_location_include_enable_checkbox = None
        if "enable_no_location_included" in self.exclusions:
            no_location_include_card, self.no_location_include_enable_checkbox = self.create_exclusion_card(
                "No Location Inclusion (Include SRs with 0,0 coordinates)", sr_types, group_descriptions,
                self.temp_selected_no_location_included_sr_types, self.temp_selected_no_location_included_groups,
                enable_toggle=True
            )
            self.no_location_include_enable_checkbox.setChecked(self.exclusions["enable_no_location_included"])  # Load saved state
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
        enable_checkbox = None

        # Add an enable checkbox at the top if specified
        if enable_toggle:
            enable_checkbox = QCheckBox(f"Enable {title}")
            enable_checkbox.setChecked(False)  # Default unchecked
            layout.addWidget(enable_checkbox)

            # Log the initial state of the enable checkbox
            initial_status = "Checked" if enable_checkbox.isChecked() else "Unchecked"
            self.logger.log_info(f"Initial state for enable checkbox '{title}': {initial_status}")

            # Connect the toggle to enable or disable the rest of the card's widgets and log changes
            enable_checkbox.toggled.connect(lambda checked: self.toggle_card_widgets(card, checked))
            enable_checkbox.toggled.connect(lambda checked: self.logger.log_info(
                f"Enable checkbox for '{title}' is {'Checked' if checked else 'Unchecked'}"
            ))

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

        return card, enable_checkbox



    def filter_list(self, list_widget, items, selected_dict, item_type):
        """Filter the QListWidget items based on the search text."""
        search_text = self.sender().text().lower()  # Get the search text from the sender (QLineEdit)
        list_widget.clear()  # Clear the current list

        # Loop through items and add only those that match the search text
        for item_id, item_data in items.items():
            if search_text in item_data["description"].lower():
                list_item = QListWidgetItem(list_widget)
                checkbox = QCheckBox(item_data["description"])
                checkbox.setChecked(selected_dict.get(item_id, False))

                # Connect state change to update the temporary selection state
                checkbox.stateChanged.connect(partial(self.update_selected_items, item_id=item_id, selected_dict=selected_dict, description=item_data["description"], item_type=item_type))

                list_widget.addItem(list_item)
                list_widget.setItemWidget(list_item, checkbox)

    def toggle_card_widgets(self, card, enabled):
        """Enable or disable all widgets within a card."""
        for widget in card.findChildren(QWidget):
            widget.setEnabled(enabled)

    def get_exclusions(self):
        """Return the current exclusions dictionary."""
        return self.exclusions

    def populate_list_with_checkboxes(self, list_widget, items, selected_dict, item_type="Item"):
        """Populate the list widget with checkboxes, setting their initial state based on selected_dict."""
        list_widget.clear()
        for item_id, item_data in items.items():
            list_item = QListWidgetItem(list_widget)
            checkbox = QCheckBox(item_data["description"])
            checkbox.setChecked(selected_dict.get(item_id, False))

            # Connect state change to update the temporary selection state and save partially
            checkbox.stateChanged.connect(partial(self.update_selected_items, item_id=item_id, selected_dict=selected_dict, description=item_data["description"], item_type=item_type))

            # Log the initial state of the checkbox
            status = "Checked" if checkbox.isChecked() else "Unchecked"
            self.logger.log_info(f"Initial state for {item_type} '{item_data['description']}' ({item_id}): {status}")

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

    def save_settings(self):
        """Save the current state of selections and enable states to the settings JSON file through AppSettings."""
        # Prepare the exclusions dictionary based on temporary selections and enable checkbox states
        self.exclusions = {
            'excluded_sr_type': [item_id for item_id, selected in self.temp_selected_excluded_sr_types.items() if selected],
            'excluded_group': [item_id for item_id, selected in self.temp_selected_excluded_groups.items() if selected],
            'no_location_excluded_sr_type': [item_id for item_id, selected in self.temp_selected_no_location_excluded_sr_types.items() if selected],
            'no_location_excluded_group': [item_id for item_id, selected in self.temp_selected_no_location_excluded_groups.items() if selected],
            'no_location_included_sr_type': [item_id for item_id, selected in self.temp_selected_no_location_included_sr_types.items() if selected],
            'no_location_included_group': [item_id for item_id, selected in self.temp_selected_no_location_included_groups.items() if selected],
            # Include enable states
            'enable_excluded': self.exclude_enable_checkbox.isChecked(),
            'enable_no_location_excluded': self.no_location_exclude_enable_checkbox.isChecked(),
            'enable_no_location_included': self.no_location_include_enable_checkbox.isChecked()
        }

        # Load current settings and update exclusions
        current_settings = self.app_settings.load_settings()
        current_settings["exclusions"] = self.exclusions
        self.app_settings.save_settings(current_settings)

        # Close the dialog
        self.accept()

    def refresh_descriptions(self):
        """Refresh the SR Type and Group descriptions, updating the lists and rebuilding JSON if Excel files have changed."""
        # Paths to the Excel files
        type_desc_path = FileHelper.get_excel_file_path("311_GIS_Type_Descriptions.xlsx")
        group_desc_path = FileHelper.get_excel_file_path("311_GIS_Group_Descriptions.xlsx")
        json_path = FileHelper.get_json_file_path("type_group_exclusion.json")

        # Check if Excel files have been updated since the last JSON build
        if FileHelper.file_modified_after(type_desc_path, json_path) or FileHelper.file_modified_after(group_desc_path, json_path):
            # Load and rebuild JSON data from Excel files
            self.logger.log_info("Excel files have been updated, rebuilding JSON data.")
            try:
                data = {
                    "type_descriptions": FileHelper.read_excel(type_desc_path) or {},
                    "group_descriptions": FileHelper.read_excel(group_desc_path) or {}
                }
                with open(json_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                self.logger.log_info("JSON data rebuilt from Excel files.")
            except Exception as e:
                self.logger.log_error(f"Failed to read Excel files: {e}")
                QMessageBox.critical(self, "Error", f"Failed to read Excel files: {e}")
                return

        # Load data from JSON to update UI components
        try:
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
                self.sr_types = data.get("type_descriptions", {}) or {}
                self.group_descriptions = data.get("group_descriptions", {}) or {}
        except Exception as e:
            self.logger.log_error(f"Error loading JSON data: {e}")
            QMessageBox.critical(self, "Error", f"Error loading JSON data: {e}")
            self.sr_types, self.group_descriptions = {}, {}

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
        self.logger.log_info("Descriptions have been refreshed and UI updated.")
