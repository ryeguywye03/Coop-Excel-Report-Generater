from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QProgressBar, QPushButton, QLabel, QDateTimeEdit, QComboBox, QScrollArea, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QDateTime
from utils import LoggerManager
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

        # Setup UI and other components
        self.setup_ui()

        # Initialize other components like file loader, report generator, etc.
        self.file_loader = FileLoader(self)
        self.report_generator = ReportGenerator(self.progress_bar)
        self.checkbox_manager = CheckboxManager(self.columns_layout)
        self.settings_handler = SettingsHandler(self)

    def setup_ui(self):
        """Set up the UI layout."""
        self.setObjectName("mainpanel")  # Set object name for the main panel
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
        sidebar_layout = QVBoxLayout()

        # Example buttons for the sidebar
        load_excel_button = QPushButton("Load Excel")
        load_excel_button.clicked.connect(self.load_excel)

        clear_excel_button = QPushButton("Clear Excel")  # Clear Excel button
        clear_excel_button.clicked.connect(self.clear_excel)

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings_dialog)

        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.main_window.switch_to_main_menu)  # Correctly reference the parent

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
        main_panel_layout = QVBoxLayout()

        # Date range selectors
        date_layout = QHBoxLayout()
        start_date_label = QLabel("Start Date:")
        self.start_date_input = QDateTimeEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDateTime(QDateTime.currentDateTime().addMonths(-1))

        end_date_label = QLabel("End Date:")
        self.end_date_input = QDateTimeEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDateTime(QDateTime.currentDateTime())

        date_layout.addWidget(start_date_label)
        date_layout.addWidget(self.start_date_input)
        date_layout.addWidget(end_date_label)
        date_layout.addWidget(self.end_date_input)

        # Column checkboxes
        columns_group = QGroupBox("Select Columns")
        self.columns_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.columns_layout)
        scroll_area.setWidget(scroll_content)

        columns_group.setLayout(self.columns_layout)

        # Sort dropdown
        self.setup_sort_dropdown(main_panel_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Buttons for generating the report
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

    def generate_report(self):
        """Calls the ReportGenerator to generate the report."""
        selected_columns = self.checkbox_manager.get_selected_columns()
        start_date = self.start_date_input.dateTime().toPyDateTime()
        end_date = self.end_date_input.dateTime().toPyDateTime()

        if selected_columns:
            self.report_generator.generate_report(self.file_loader.df, selected_columns, start_date, end_date)

    def preview_report(self):
        """Generates and shows a preview of the report."""
        # Check if the Excel file has been loaded
        if not hasattr(self.file_loader, 'df') or self.file_loader.df is None:
            QMessageBox.warning(self, "No Data", "Please load an Excel file first before previewing the report.")
            return

        selected_columns = self.checkbox_manager.get_selected_columns()
        if not selected_columns:
            QMessageBox.warning(self, "Warning", "No columns selected for the preview.")
            return

        try:
            start_date = self.start_date_input.dateTime().toPyDateTime()
            end_date = self.end_date_input.dateTime().toPyDateTime()

            if start_date > end_date:
                QMessageBox.critical(self, "Error", "Start date cannot be after end date")
                return

            # Generate the report using ReportGenerator
            report_df = self.report_generator.generate_report(self.file_loader.df, selected_columns, start_date, end_date)

            # Call the ReportGenerator to show the report preview
            if report_df is not None:
                self.report_generator.show_report_preview(report_df)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating preview: {e}")

    def load_excel(self):
        """Delegate the Excel file loading to the FileLoader class."""
        self.file_loader.load_file()  # Call the load_file method from FileLoader
        self.populate_sort_by_dropdown()

    def clear_excel(self):
        """Clear the loaded Excel file and reset the UI."""
        self.file_loader.df = None
        self.sort_by_dropdown.clear()
        self.sort_by_dropdown.setEnabled(False)
        self.checkbox_manager.clear_checkboxes()  # Clear checkboxes
        self.logger.log_info("Excel file cleared.")

    def populate_sort_by_dropdown(self):
        """Populate the Sort By dropdown with the columns from the loaded Excel file."""
        if self.file_loader.df is not None:
            self.sort_by_dropdown.clear()
            self.sort_by_dropdown.addItems(self.file_loader.df.columns)
            self.sort_by_dropdown.setEnabled(True)  # Enable dropdown after loading columns

    def open_settings_dialog(self):
        """Open the settings dialog by using the SettingsHandler."""
        self.settings_handler.open_settings_dialog()

    def remove_extra_widget(self):
        """Ensure any extra, unnecessary widgets are removed."""
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget and isinstance(widget, QGroupBox):
                # Identify the empty/extra widget and remove it
                if widget.title() == "":
                    widget.deleteLater()
                    break
