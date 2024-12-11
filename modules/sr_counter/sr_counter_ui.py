from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QGroupBox, QProgressBar, QPushButton, QLabel,
    QDateEdit, QTimeEdit, QComboBox, QScrollArea, QHBoxLayout, QMessageBox, QCheckBox
)
from PyQt6.QtCore import QDateTime, QTime, Qt
from modules.utils.logger_manager import LoggerManager
from modules.utils.app_settings import AppSettings
from ..utils.file_loader import FileLoader
from .report_generator import ReportGenerator
from ..utils.checkbox_manager import CheckboxManager
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

    def on_sort_by_changed(self):
        """Updates the selected_sort_by variable when the dropdown selection changes."""
        self.selected_sort_by = self.sort_by_dropdown.currentText()
        self.logger.log_info(f"Sort By changed to: {self.selected_sort_by}")

    def setup_ui(self):
        """Set up the UI layout."""
        self.setObjectName("mainPanel")  # Main panel object name
        self.main_layout = QGridLayout(self)

        # Set up the sidebar and main panel
        sidebar = self.setup_sidebar()
        sr_counter_panel = self.setup_main_panel()

        self.main_layout.addWidget(sidebar, 0, 0, 1, 1)
        self.main_layout.addWidget(sr_counter_panel, 0, 1, 1, 2)

    def setup_sidebar(self):
        """Set up the sidebar specific to SR Counter."""
        sidebar_group = QGroupBox("SR Counter Options")
        sidebar_group.setObjectName("sidebarGroup")
        sidebar_layout = QVBoxLayout()

        # Load Excel Button
        load_excel_button = QPushButton("Load Excel")
        load_excel_button.setProperty("class", "sidebar-button")  # Apply reusable class
        load_excel_button.clicked.connect(self.load_excel)

        # Clear Excel Button
        clear_excel_button = QPushButton("Clear Excel")
        clear_excel_button.setProperty("class", "sidebar-button")  # Apply reusable class
        clear_excel_button.clicked.connect(self.clear_excel)

        # Settings Button
        settings_button = QPushButton("Settings")
        settings_button.setProperty("class", "sidebar-button")  # Apply reusable class
        settings_button.clicked.connect(self.open_settings_dialog)

        # Back Button
        back_button = QPushButton("Back to Main Menu")
        back_button.setProperty("class", "sidebar-button")  # Apply reusable class
        back_button.clicked.connect(self.main_window.switch_to_main_menu)

        # Add Buttons
        sidebar_layout.addWidget(load_excel_button)
        sidebar_layout.addWidget(clear_excel_button)
        sidebar_layout.addWidget(settings_button)
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
        sort_label.setProperty("class", "label")  # Apply reusable class
        self.sort_by_dropdown = QComboBox()
        self.sort_by_dropdown.setProperty("class", "dropdown")  # Apply reusable class
        self.sort_by_dropdown.addItems(["Type Description", "Group Description", "Created Date"])
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_by_dropdown)
        main_panel_layout.addLayout(sort_layout)
        self.sort_by_dropdown.currentIndexChanged.connect(self.on_sort_by_changed)

        # Date selectors (start and end)
        date_layout = QHBoxLayout()
        start_date_label = QLabel("Start Date:")
        start_date_label.setProperty("class", "label")  # Apply reusable class
        self.start_date_input = QDateEdit()
        self.start_date_input.setProperty("class", "input-field")  # Apply reusable class
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDateTime.currentDateTime().addMonths(-1).date())

        end_date_label = QLabel("End Date:")
        end_date_label.setProperty("class", "label")  # Apply reusable class
        self.end_date_input = QDateEdit()
        self.end_date_input.setProperty("class", "input-field")  # Apply reusable class
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDateTime.currentDateTime().date())

        date_layout.addWidget(start_date_label)
        date_layout.addWidget(self.start_date_input)
        date_layout.addWidget(end_date_label)
        date_layout.addWidget(self.end_date_input)
        main_panel_layout.addLayout(date_layout)

        # Time frame toggle and dropdowns (below date selectors)
        time_frame_layout = QHBoxLayout()
        self.use_time_checkbox = QCheckBox("Enable Time Frame")
        self.use_time_checkbox.setProperty("class", "checkbox")  # Apply reusable class
        self.use_time_checkbox.stateChanged.connect(self.toggle_time_frame)

        start_time_label = QLabel("Start Time:")
        start_time_label.setProperty("class", "label")  # Apply reusable class
        self.start_time_input = QTimeEdit()
        self.start_time_input.setProperty("class", "input-field")  # Apply reusable class
        self.start_time_input.setEnabled(False)

        end_time_label = QLabel("End Time:")
        end_time_label.setProperty("class", "label")  # Apply reusable class
        self.end_time_input = QTimeEdit()
        self.end_time_input.setProperty("class", "input-field")  # Apply reusable class
        self.end_time_input.setEnabled(False)

        self.start_time_input.setTime(QTime(0, 0))
        self.end_time_input.setTime(QTime(23, 59))

        time_frame_layout.addWidget(self.use_time_checkbox)
        time_frame_layout.addWidget(start_time_label)
        time_frame_layout.addWidget(self.start_time_input)
        time_frame_layout.addWidget(end_time_label)
        time_frame_layout.addWidget(self.end_time_input)
        main_panel_layout.addLayout(time_frame_layout)

        # Column checkboxes in a scrollable area
        columns_group = QGroupBox("Select Columns")
        columns_group.setObjectName("columnsGroup")
        scroll_area = QScrollArea()
        scroll_area.setProperty("class", "scroll-area")  # Apply reusable class
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(200)

        scroll_content = QWidget()
        scroll_content.setObjectName("scrollContent")
        self.columns_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(self.columns_layout)
        scroll_area.setWidget(scroll_content)

        columns_group_layout = QVBoxLayout(columns_group)
        columns_group_layout.addWidget(scroll_area)
        main_panel_layout.addWidget(columns_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setProperty("class", "progress-bar")  # Apply reusable class
        self.progress_bar.setValue(0)
        main_panel_layout.addWidget(self.progress_bar)

        # Buttons for generating the report
        button_layout = QHBoxLayout()
        preview_button = QPushButton("Preview Report")
        preview_button.setProperty("class", "report-button")  # Apply reusable class
        preview_button.clicked.connect(self.preview_report)

        generate_button = QPushButton("Generate Report")
        generate_button.setProperty("class", "report-button")  # Apply reusable class
        generate_button.clicked.connect(self.generate_report)

        button_layout.addWidget(preview_button)
        button_layout.addWidget(generate_button)

        main_panel_layout.addLayout(button_layout)

        sr_counter_group.setLayout(main_panel_layout)
        return sr_counter_group




    def toggle_time_frame(self):
        """Enable or disable the time frame dropdowns."""
        is_enabled = self.use_time_checkbox.isChecked()
        self.start_time_input.setEnabled(is_enabled)
        self.end_time_input.setEnabled(is_enabled)

        # Reset to default "all time" if disabled
        if not is_enabled:
            self.start_time_input.setTime(QTime(0, 0))
            self.end_time_input.setTime(QTime(23, 59))




    def validate_time_columns(self):
        """Validate if time columns exist when time frame is enabled."""
        if not self.use_time_checkbox.isChecked():
            return
        if not self.file_loader.validate_time_columns():
            self.use_time_checkbox.setChecked(False)

    def generate_report(self):
        """Generate the report based on selected criteria."""
        selected_columns = self.checkbox_manager.get_selected_columns()
        if not selected_columns:
            QMessageBox.warning(self, "Warning", "Please select columns for the report.")
            return

        # Fetch start and end dates
        start_date = self.start_date_input.dateTime().toPyDateTime()
        end_date = self.end_date_input.dateTime().toPyDateTime()

        # Fetch start and end times if time frame is enabled
        start_time = self.start_time_input.time().toPyTime() if self.use_time_checkbox.isChecked() else None
        end_time = self.end_time_input.time().toPyTime() if self.use_time_checkbox.isChecked() else None

        # Validate time range if time frame is enabled
        if start_time and end_time and start_time > end_time:
            QMessageBox.critical(self, "Error", "Start Time cannot be after End Time.")
            return

        try:
            # Generate the report
            report_df = self.report_generator.generate_report(
                self.file_loader.df, selected_columns, start_date, end_date, start_time, end_time, sort_by=self.selected_sort_by
            )
            if report_df is not None:
                # Save the report, passing time frame details
                output_file = self.report_generator.save_report(report_df, start_date, end_date, start_time, end_time)
                if output_file:  # Alert only after successful save
                    QMessageBox.information(self, "Success", f"Report saved at {output_file}")
        except Exception as e:
            self.logger.log_error(f"Error during report generation: {e}")
            QMessageBox.critical(self, "Error", "Failed to generate report.")



    def preview_report(self):
        """Preview the report based on current settings."""
        if self.file_loader.df is None:
            QMessageBox.warning(self, "No Data", "Please load a file first.")
            return

        selected_columns = self.checkbox_manager.get_selected_columns()
        if not selected_columns:
            QMessageBox.warning(self, "Warning", "No columns selected for preview.")
            return

        # Fetch start and end dates
        start_date = self.start_date_input.dateTime().toPyDateTime()
        end_date = self.end_date_input.dateTime().toPyDateTime()

        # Fetch start and end times if time frame is enabled
        start_time = self.start_time_input.time().toPyTime() if self.use_time_checkbox.isChecked() else None
        end_time = self.end_time_input.time().toPyTime() if self.use_time_checkbox.isChecked() else None

        # Validate time range if time frame is enabled
        if start_time and end_time and start_time > end_time:
            QMessageBox.critical(self, "Error", "Start Time cannot be after End Time.")
            return

        try:
            # Generate and preview the report
            report_df = self.report_generator.generate_report(
                self.file_loader.df, selected_columns, start_date, end_date, start_time, end_time, sort_by=self.selected_sort_by
            )
            if report_df is not None:
                self.report_generator.show_report_preview(report_df)
        except Exception as e:
            self.logger.log_error(f"Error during preview: {e}")
            QMessageBox.critical(self, "Error", "Failed to preview report.")


    def load_excel(self):
        """Delegate file loading to FileLoader."""
        self.file_loader.load_file()
        if self.file_loader.df is not None:
            self.populate_sort_by_dropdown()

    def clear_excel(self):
        """Clear the loaded file and reset UI."""
        self.file_loader.df = None
        self.sort_by_dropdown.clear()
        self.checkbox_manager.clear_checkboxes()

    def populate_sort_by_dropdown(self):
        """Populate the dropdown with column headers."""
        if self.file_loader.df is not None:
            self.sort_by_dropdown.clear()
            self.sort_by_dropdown.addItems(self.file_loader.df.columns)

    def open_settings_dialog(self):
        """Open settings dialog."""
        self.settings_handler.open_settings_dialog()
