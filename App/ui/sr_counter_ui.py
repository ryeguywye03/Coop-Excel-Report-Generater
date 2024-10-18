from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QDateTimeEdit, QCheckBox, QProgressBar, QFileDialog, QMessageBox, QScrollArea, QGroupBox, QPushButton, QSizePolicy, QComboBox
from PyQt5.QtCore import QDateTime
import pandas as pd
import json
from logic.logger_manager import LoggerManager
from logic.sr_count import SRReportGenerator
from ui.report_preview import ReportPreview  # Import the ReportPreview dialog
from config.settings_manager import SettingsManager
from ui.settings_dialog import SettingsDialog
from utils import resource_path  # Import the resource path utility function
import logging
import os


class SRCounterUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent  # Store the reference to the main window
        
        # Setup UI and get the progress bar from the main panel
        self.setup_ui()

        # Set up a logger
        self.logger = LoggerManager()

        # Initialize the report generator with the existing progress bar and logger
        self.report_generator = SRReportGenerator(self.progress_bar)

        self.settings_manager = SettingsManager()

        # Initialize the exclusions (to be populated from the settings dialog)
        self.exclusions = {"excluded_sr_type": [], "excluded_group": []}

    def setup_ui(self):
        self.setObjectName("mainpanel")  # Set object name for styling
        self.main_layout = QGridLayout(self)

        # Setup main panel
        sr_counter_panel = self.setup_main_panel()  # Main content panel

        # Add main content to the layout
        self.main_layout.addWidget(sr_counter_panel, 0, 1, 1, 2)  # Main panel on the right

        # Set stretch factors for main panel
        self.main_layout.setColumnStretch(1, 1)  # Main panel expands

    def setup_sidebar(self):
        """Set up the sidebar for SR Counter UI."""
        sidebar_group = QGroupBox("SR Counter Options")
        sidebar_layout = QVBoxLayout()

        # Back to Main Menu Button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.main_window.switch_to_main_menu)

        # Load Excel Button
        load_excel_button = QPushButton("Load Excel")
        load_excel_button.clicked.connect(self.load_file)

        # Settings Button
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings_dialog)

        # Add buttons to sidebar layout
        sidebar_layout.addWidget(load_excel_button)
        sidebar_layout.addWidget(settings_button)
        sidebar_layout.addWidget(back_button)

        sidebar_group.setLayout(sidebar_layout)
        return sidebar_group

    def setup_main_panel(self):
        """Set up the main content area for SR Counter UI."""
        sr_counter_group = QGroupBox("SR Counter")
        main_panel_layout = QVBoxLayout()

        # Date range inputs
        date_layout = QHBoxLayout()
        start_date_label = QLabel("Start Date:")
        self.start_date_input = QDateTimeEdit()
        self.start_date_input.setCalendarPopup(True)

        today = QDateTime.currentDateTime()
        self.start_date_input.setDateTime(today.addMonths(-1))  # Default to one month ago
        
        end_date_label = QLabel("End Date:")
        self.end_date_input = QDateTimeEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDateTime(today)  # Default to today

        date_layout.addWidget(start_date_label)
        date_layout.addWidget(self.start_date_input)
        date_layout.addWidget(end_date_label)
        date_layout.addWidget(self.end_date_input)

        # Add column selection checkboxes
        columns_group = QGroupBox("Select Columns")
        self.columns_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.columns_layout)
        scroll_area.setWidget(scroll_content)

        columns_group.setLayout(self.columns_layout)

        # Use the existing progress bar at the bottom of the panel
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Add the sort dropdown before the buttons
        self.setup_sort_dropdown(main_panel_layout)

        # Buttons for report generation
        button_layout = QHBoxLayout()
        preview_button = QPushButton("Preview Report")
        preview_button.clicked.connect(self.preview_report)

        generate_button = QPushButton("Generate Report")
        generate_button.clicked.connect(self.generate_report)

        button_layout.addWidget(preview_button)
        button_layout.addWidget(generate_button)

        # Add all elements to the main panel layout
        main_panel_layout.addLayout(date_layout)
        main_panel_layout.addWidget(columns_group)
        main_panel_layout.addWidget(self.progress_bar)
        main_panel_layout.addLayout(button_layout)

        sr_counter_group.setLayout(main_panel_layout)
        return sr_counter_group

    def setup_sort_dropdown(self, main_panel_layout):
        """Creates a dropdown to allow the user to select a column to sort the report by."""
        # Create a label for the dropdown
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort By:")
        sort_label.setObjectName("sort_by_label")  # For QSS styling, if needed
        
        # Create a dropdown for sorting columns
        self.sort_by_dropdown = QComboBox(self)
        self.sort_by_dropdown.setObjectName("sort_by_dropdown")  # For QSS styling

        # Initially disable the dropdown until columns are loaded
        self.sort_by_dropdown.setEnabled(False)

        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_by_dropdown)
        # Add the sort dropdown to the layout above the progress bar
        main_panel_layout.addLayout(sort_layout)

    def get_sort_column(self):
        """Retrieve the selected column to sort by from the dropdown."""
        selected_sort_column = self.sort_by_dropdown.currentText()
        if selected_sort_column == "Select column":
            return None  # No valid selection
        return selected_sort_column

    
    def open_settings_dialog(self):
        """Open the settings dialog, handling errors for missing JSON files."""
        try:
            json_path = resource_path(os.path.join('assets', 'json', 'type_group_exclusion.json'))

            # Load the JSON data
            with open(json_path, 'r') as f:
                data = json.load(f)

            sr_types = data.get("type_descriptions", {})
            group_descriptions = data.get("group_descriptions", {})

            dialog = SettingsDialog(self, sr_types, group_descriptions)

            if dialog.exec_():  # Show the dialog and wait for the user to press OK
                # Ensure the correct structure for exclusions
                self.exclusions = {
                    'excluded_sr_type': dialog.exclusions.get('excluded_sr_types', []),
                    'excluded_group': dialog.exclusions.get('excluded_groups', []),
                    'no_location_excluded_sr_type': dialog.exclusions.get('no_location_excluded_sr_types', []),
                    'no_location_excluded_group': dialog.exclusions.get('no_location_excluded_groups', [])
                }

                print(f"Excluding SR Types: {self.exclusions.get('excluded_sr_type', [])}")
                print(f"Excluding Groups: {self.exclusions.get('excluded_group', [])}")
                print(f"Excluding No Location SR Types: {self.exclusions.get('no_location_excluded_sr_type', [])}")
                print(f"Excluding No Location Groups: {self.exclusions.get('no_location_excluded_group', [])}")

        except FileNotFoundError as e:
            self.logger.log_error(f"Error loading JSON file: {str(e)}")
            QMessageBox.critical(self, "File Not Found", f"Error: {str(e)}\nThe required JSON file could not be found.")
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Error parsing JSON file: {str(e)}")
            QMessageBox.critical(self, "JSON Parsing Error", f"Error: {str(e)}\nThe JSON file could not be parsed correctly.")



    def refresh_json_file(self):
        """Method to refresh or create the JSON file from Excel sources."""
        try:
            self.settings_manager.create_json_from_excel()
            QMessageBox.information(self, "Success", "The settings file has been refreshed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while refreshing the settings file: {str(e)}")

    def load_file(self):
        """Open the file dialog to load an Excel file and dynamically generate column checkboxes."""
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
            if file_path:
                self.df = self.load_excel(file_path)
                self.create_checkboxes()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load Excel file: {e}")

    def load_excel(self, file_path):
        """Load the Excel file into a DataFrame."""
        try:
            if file_path.endswith('.xls'):
                df = pd.read_excel(file_path, engine='xlrd')
            else:
                df = pd.read_excel(file_path, engine='openpyxl')

            # Filter and rename columns as needed
            column_mapping = {
                'Service_Re': 'Service Request Number',
                'Created_Da': 'Created Date',
                'Type_Descr': 'Type Description',
                'Group_Desc': 'Group Description',
                'X_Value': 'X Value',
                'Y_Value': 'Y Value'
            }
            df = df.rename(columns=column_mapping)

            required_columns = ["Service Request Number", "Created Date", "Type Description", "Group Description", "X Value", "Y Value"]
            if all(column in df.columns for column in required_columns):
                return df[required_columns]
            else:
                missing_columns = [column for column in required_columns if column not in df.columns]
                QMessageBox.critical(self, "Error", f"Required columns are missing: {', '.join(missing_columns)}")
                return None

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load Excel file: {e}")
            return None

    def create_checkboxes(self):
        """Create checkboxes for each column in the loaded Excel file."""
        if self.df is None:
            return  # If no DataFrame, do not attempt to create checkboxes

        # Clear existing checkboxes
        for i in reversed(range(self.columns_layout.count())):
            widget = self.columns_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Create new checkboxes based on the loaded DataFrame's columns
        self.checkboxes = []
        for col in self.df.columns:
            checkbox = QCheckBox(col)
            checkbox.setStyleSheet("margin-bottom: 5px;")  # Reduce spacing between checkboxes
            self.columns_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        # Enable and populate the sorting dropdown once columns are loaded
        self.sort_by_dropdown.setEnabled(True)
        self.sort_by_dropdown.clear()  # Clear previous options
        self.sort_by_dropdown.addItems([col for col in self.df.columns])

    def preview_report(self):
        """Show a preview of the report by calling the ReportPreview dialog."""
        # Check if the DataFrame (df) exists
        if not hasattr(self, 'df') or self.df is None:
            QMessageBox.warning(self, "No Data", "Please load an Excel file first before previewing the report.")
            return

        if not self.checkboxes:
            QMessageBox.warning(self, "No Data", "Please load a file and select columns first.")
            return

        selected_columns = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        if not selected_columns:
            QMessageBox.warning(self, "Warning", "No columns selected for the preview.")
            return

        # Get the sort by column
        sort_by_column = self.get_sort_column()

        try:
            start_date = self.start_date_input.dateTime().toPyDateTime()
            end_date = self.end_date_input.dateTime().toPyDateTime()

            if start_date > end_date:
                QMessageBox.critical(self, "Error", "Start date cannot be after end date")
                return

            # Exclude rows based on exclusions from settings
            df_filtered = self.df[~((self.df['Type Description'].isin(self.exclusions['excluded_sr_type'])) |
                                (self.df['Group Description'].isin(self.exclusions['excluded_group'])))]

            # Call the generate_report function to filter and generate the report DataFrame
            report_df = self.report_generator.generate_report(df_filtered, selected_columns, start_date, end_date, sort_by_column)

            # Call the ReportPreview dialog (from report_preview.py) to display the report
            if report_df is not None:
                dialog = ReportPreview(self, report_df)
                dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating preview: {e}")


    def generate_report(self):
        """Generate and save the report based on the selected columns and date range."""
        if self.df is None or not self.checkboxes:
            QMessageBox.warning(self, "No Data", "Please load a file and select columns first.")
            return

        selected_columns = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        if not selected_columns:
            QMessageBox.warning(self, "Warning", "No columns selected for the report.")
            return

        # Get the sort by column
        sort_by_column = self.get_sort_column()

        try:
            start_date = self.start_date_input.dateTime().toPyDateTime()
            end_date = self.end_date_input.dateTime().toPyDateTime()

            if start_date > end_date:
                QMessageBox.critical(self, "Error", "Start date cannot be after end date")
                return

            # Exclude rows based on exclusions from settings
            df_filtered = self.df[~((self.df['Type Description'].isin(self.exclusions['excluded_sr_type'])) |
                                   (self.df['Group Description'].isin(self.exclusions['excluded_group'])))]

            # Call the report generator from sr_count.py
            report_df = self.report_generator.generate_report(df_filtered, selected_columns, start_date, end_date, sort_by_column)

            # Save the report
            output_file = self.report_generator.save_report(report_df)
            if output_file:
                QMessageBox.information(self, "Success", f"Report saved as {output_file}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating report: {e}")

