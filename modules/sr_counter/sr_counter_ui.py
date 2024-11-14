from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QGroupBox, QProgressBar, QPushButton, QLabel,
    QDateTimeEdit, QComboBox, QScrollArea, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import QDateTime, QTime, Qt
from modules.utils.logger_manager import LoggerManager
from modules.utils.app_settings import AppSettings  # Use AppSettings for unified configuration
from .file_loader import FileLoader
from .report_generator import ReportGenerator
from .checkbox_manager import CheckboxManager
from .settings_handler import SettingsHandler

class SRCounterUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent

        # Initialize logger
        self.logger = LoggerManager()
        
        # Initialize AppSettings for shared settings access
        self.settings = AppSettings()
        
        # Setup UI and other components
        self.setup_ui()

        # Initialize other components like file loader, report generator, etc.
        self.file_loader = FileLoader(self)
        self.report_generator = ReportGenerator(self.progress_bar)
        self.checkbox_manager = CheckboxManager(self.columns_layout)
        self.settings_handler = SettingsHandler(self)

        # Variable to track the selected sort column
        self.selected_sort_by = None

    def setup_ui(self):
        """Set up the UI layout."""
        self.setObjectName("mainPanel")  # Main panel object name
        self.main_layout = QGridLayout(self)
        
        # Set up the sidebar and main panel
        sidebar = self.setup_sidebar()  # Ensure sidebar is created only once
        sr_counter_panel = self.setup_main_panel()

        # Add sidebar and main panel to the main layout
        self.main_layout.addWidget(sidebar, 0, 0, 1, 1)  # Add sidebar once on the left
        self.main_layout.addWidget(sr_counter_panel, 0, 1, 1, 2)  # Add main panel next to sidebar

    def setup_sidebar(self):
        """Set up the sidebar specific to SR Counter."""
        sidebar_group = QGroupBox("SR Counter Options")
        sidebar_group.setObjectName("sidebarGroup")
        sidebar_layout = QVBoxLayout()

        # Example buttons for the sidebar
        load_excel_button = QPushButton("Load Excel")
        load_excel_button.setObjectName("loadExcelButton")
        load_excel_button.clicked.connect(self.load_excel)

        clear_excel_button = QPushButton("Clear Excel")
        clear_excel_button.setObjectName("clearExcelButton")
        clear_excel_button.clicked.connect(self.clear_excel)

        settings_button = QPushButton("Settings")
        settings_button.setObjectName("settingsButton")
        settings_button.clicked.connect(self.open_settings_dialog)

        back_button = QPushButton("Back to Main Menu")
        back_button.setObjectName("backButton")
        back_button.clicked.connect(self.main_window.switch_to_main_menu)

        # Add buttons to the sidebar layout
        sidebar_layout.addWidget(load_excel_button)
        sidebar_layout.addWidget(clear_excel_button)
        sidebar_layout.addWidget(settings_button)

        # Add a stretch to push the back button to the bottom
        sidebar_layout.addStretch(1)
        sidebar_layout.addWidget(back_button)

        sidebar_group.setLayout(sidebar_layout)
        return sidebar_group

    def setup_main_panel(self):
        """Set up the main content area for SR Counter UI."""
        sr_counter_group = QGroupBox("SR Counter")
        sr_counter_group.setObjectName("srCounterGroup")
        main_panel_layout = QVBoxLayout()

        # Sort dropdown
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort By:")
        sort_label.setObjectName("sortLabel")
        self.sort_by_dropdown = QComboBox()
        self.sort_by_dropdown.setObjectName("sortByDropdown")
        self.sort_by_dropdown.addItems(["Type Description", "Group Description", "Created Date"])
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_by_dropdown)
        main_panel_layout.addLayout(sort_layout)
        self.sort_by_dropdown.currentIndexChanged.connect(self.on_sort_by_changed)

        # Date range selectors
        date_layout = QHBoxLayout()
        start_date_label = QLabel("Start Date:")
        start_date_label.setObjectName("startDateLabel")
        self.start_date_input = QDateTimeEdit()
        self.start_date_input.setObjectName("startDateInput")
        self.start_date_input.setCalendarPopup(True)
        start_date_time = QDateTime.currentDateTime().addMonths(-1)
        start_date_time.setTime(QTime(8, 0))
        self.start_date_input.setDateTime(start_date_time)
        self.start_date_input.dateTimeChanged.connect(self.set_start_time)

        end_date_label = QLabel("End Date:")
        end_date_label.setObjectName("endDateLabel")
        self.end_date_input = QDateTimeEdit()
        self.end_date_input.setObjectName("endDateInput")
        self.end_date_input.setCalendarPopup(True)
        end_date_time = QDateTime.currentDateTime()
        end_date_time.setTime(QTime(16, 0))
        self.end_date_input.setDateTime(end_date_time)
        self.end_date_input.dateTimeChanged.connect(self.set_end_time)

        date_layout.addWidget(start_date_label)
        date_layout.addWidget(self.start_date_input)
        date_layout.addWidget(end_date_label)
        date_layout.addWidget(self.end_date_input)
        main_panel_layout.addLayout(date_layout)

        # Column checkboxes in a scrollable area
        columns_group = QGroupBox("Select Columns")
        columns_group.setObjectName("columnsGroup")
        scroll_area = QScrollArea()
        scroll_area.setObjectName("columnsScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(200)

        # Create a widget for the checkboxes and add it to the scroll area
        scroll_content = QWidget()
        scroll_content.setObjectName("scrollContent")
        self.columns_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(self.columns_layout)
        scroll_area.setWidget(scroll_content)

        columns_group_layout = QVBoxLayout(columns_group)
        columns_group_layout.addWidget(scroll_area)
        main_panel_layout.addWidget(columns_group)

        # Initialize CheckboxManager without predefined columns
        self.checkbox_manager = CheckboxManager(self.columns_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setValue(0)
        main_panel_layout.addWidget(self.progress_bar)

        # Buttons for generating the report
        button_layout = QHBoxLayout()
        preview_button = QPushButton("Preview Report")
        preview_button.setObjectName("previewButton")
        preview_button.clicked.connect(self.preview_report)

        generate_button = QPushButton("Generate Report")
        generate_button.setObjectName("generateButton")
        generate_button.clicked.connect(self.generate_report)

        button_layout.addWidget(preview_button)
        button_layout.addWidget(generate_button)

        main_panel_layout.addLayout(button_layout)

        sr_counter_group.setLayout(main_panel_layout)
        return sr_counter_group

    def on_sort_by_changed(self):
        """Updates the selected_sort_by variable when the dropdown selection changes."""
        self.selected_sort_by = self.sort_by_dropdown.currentText()
        self.logger.log_info(f"Sort By changed to: {self.selected_sort_by}")

    def generate_report(self):
        """Generates the report based on selected sort column and other criteria."""
        if not self.selected_sort_by:
            self.selected_sort_by = self.sort_by_dropdown.currentText()

        selected_columns = self.checkbox_manager.get_selected_columns()
        start_date = self.start_date_input.dateTime().toPyDateTime()
        end_date = self.end_date_input.dateTime().toPyDateTime()

        if not selected_columns:
            QMessageBox.warning(self, "Warning", "Please select columns for the report.")
            return

        if not hasattr(self.file_loader, 'df') or self.file_loader.df is None:
            QMessageBox.warning(self, "No Data", "Please load an Excel file first before generating the report.")
            return

        self.logger.log_info(f"Generating report with sort column: {self.selected_sort_by}")

        try:
            report_df = self.report_generator.generate_report(
                self.file_loader.df, selected_columns, start_date, end_date, sort_by=self.selected_sort_by
            )
            
            if report_df is not None:
                output_file = self.report_generator.save_report(report_df)
                if output_file:
                    QMessageBox.information(self, "Success", f"Report saved at {output_file}")
                else:
                    QMessageBox.warning(self, "Error", "Report could not be saved. Check logs for details.")
            else:
                QMessageBox.warning(self, "Error", "Report generation failed. Check logs for details.")
        
        except Exception as e:
            self.logger.log_error(f"Error during report generation: {e}")
            QMessageBox.critical(self, "Error", f"Failed to generate report: {e}")


    def preview_report(self):
        """Generates and shows a preview of the report based on current settings."""
        if not hasattr(self.file_loader, 'df') or self.file_loader.df is None:
            QMessageBox.warning(self, "No Data", "Please load an Excel file first before previewing the report.")
            return

        selected_columns = self.checkbox_manager.get_selected_columns()
        if not selected_columns:
            self.logger.log_warning("No columns selected for the preview.")
            QMessageBox.warning(self, "Warning", "No columns selected for the preview.")
            return

        start_date = self.start_date_input.dateTime().toPyDateTime()
        end_date = self.end_date_input.dateTime().toPyDateTime()

        if start_date > end_date:
            QMessageBox.critical(self, "Error", "Start date cannot be after end date.")
            return

        if not self.selected_sort_by:
            self.selected_sort_by = self.sort_by_dropdown.currentText()

        self.logger.log_info(f"Preview Report - Sort By: {self.selected_sort_by}")

        try:
            report_df = self.report_generator.generate_report(
                self.file_loader.df, selected_columns, start_date, end_date, sort_by=self.selected_sort_by
            )
            
            if report_df is not None:
                self.report_generator.show_report_preview(report_df)
            else:
                QMessageBox.warning(self, "Error", "Report generation failed. Check logs for details.")
        except Exception as e:
            self.logger.log_error(f"Error generating preview: {e}")
            QMessageBox.critical(self, "Error", f"Error generating preview: {e}")


    def load_excel(self):
        """Delegate the Excel file loading to the FileLoader class."""
        self.file_loader.load_file()
        if self.file_loader.df is not None:
            self.logger.log_info("Excel file loaded successfully.")
            self.populate_sort_by_dropdown()  # Populate the sort dropdown with columns
        else:
            self.logger.log_warning("No data found in loaded Excel file.")

    def set_start_time(self):
        """Set the start time to 8:00 AM whenever the date is changed."""
        current_date = self.start_date_input.dateTime()
        current_date.setTime(QTime(8, 0))  # Set time to 8:00 AM
        self.start_date_input.setDateTime(current_date)  # Update the QDateTimeEdit with the modified date

    def set_end_time(self):
        """Set the end time to 4:00 PM whenever the date is changed."""
        current_date = self.end_date_input.dateTime()
        current_date.setTime(QTime(16, 0))  # Set time to 4:00 PM
        self.end_date_input.setDateTime(current_date)  # Update the QDateTimeEdit with the modified date

    def clear_excel(self):
        """Clear the loaded Excel file and reset the UI."""
        self.file_loader.df = None
        self.sort_by_dropdown.clear()
        self.sort_by_dropdown.setEnabled(False)
        self.checkbox_manager.clear_checkboxes()
        self.logger.log_info("Excel file cleared.")

    def populate_sort_by_dropdown(self):
        """Populate the Sort By dropdown with the columns from the loaded Excel file."""
        if self.file_loader.df is not None:
            self.sort_by_dropdown.clear()
            self.sort_by_dropdown.addItems(self.file_loader.df.columns)  # Add columns dynamically
            self.sort_by_dropdown.setEnabled(True)
            self.sort_by_dropdown.setCurrentIndex(0)  # Set the first item as the default selection
            self.selected_sort_by = self.sort_by_dropdown.currentText()
            self.logger.log_info(f"Dropdown populated with columns: {self.file_loader.df.columns}, defaulted to: {self.selected_sort_by}")

    def open_settings_dialog(self):
        """Open the settings dialog by using the SettingsHandler."""
        self.settings_handler.open_settings_dialog()

    def remove_extra_widget(self):
        """Ensure any extra, unnecessary widgets are removed."""
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget and isinstance(widget, QGroupBox):
                if widget.title() == "":
                    widget.deleteLater()
                    break
