import sys
import os
import logging
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QFileDialog, QCheckBox, QProgressBar, QMessageBox, QComboBox, QGridLayout, 
    QGroupBox, QDateTimeEdit, QStackedWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QDialog, QLineEdit, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QDateTime, Qt
from sr_count import SRReportGenerator

# Setup the logger
logging.basicConfig(
    filename='app_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ReportGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Excel Report Generator")
        self.setGeometry(100, 100, 1100, 580)

        # Initialize central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout for the window
        self.main_layout = QGridLayout(self.central_widget)

        # Initialize variables
        self.df = None
        self.column_checkboxes = []
        self.selected_columns = []

        # Create the StackedWidget to hold multiple content views
        self.content_area = QStackedWidget()

        # Create the Welcome Page
        self.create_welcome_page()

        # Create the SR Counter Page
        self.create_sr_counter_page()

        # Create instance of SRReportGenerator
        # Inside the ReportGeneratorApp __init__ method
        # Initialize the logger and pass it along with the progress bar
        self.logger = logging.getLogger(__name__)
        self.report_generator = SRReportGenerator(self.progress_bar, self.logger)


        # Create the sidebar navigation
        self.sidebar_group = QGroupBox("Menu")
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_group.setLayout(self.sidebar_layout)

        self.create_sidebar_main_menu()  # Start with the main menu

        # Add widgets to main layout
        self.main_layout.addWidget(self.sidebar_group, 0, 0, 1, 1)  # Sidebar
        self.main_layout.addWidget(self.content_area, 0, 1, 1, 2)   # Main content
        self.content_area.setCurrentWidget(self.welcome_page)  # Set the default page to the welcome page

    def create_sidebar_main_menu(self):
        """Create the main menu sidebar with only the 'SR Counter' button."""
        self.clear_sidebar()

        # SR Counter button (Main Menu) - Placed at the top
        self.sr_counter_button = QPushButton("SR Counter")
        self.sr_counter_button.clicked.connect(self.show_sr_counter_page)
        self.sidebar_layout.addWidget(self.sr_counter_button)

        # Add spacer to push any additional items to the bottom
        self.sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_sidebar_sr_counter(self):
        """Create the SR Counter sidebar with Load, Generate, Preview, Back, and Settings buttons."""
        self.clear_sidebar()

        # Load Excel button
        self.load_button = QPushButton("Load Excel File")
        self.load_button.clicked.connect(self.open_file_and_load)
        self.sidebar_layout.addWidget(self.load_button)

        # Generate report button
        self.generate_button = QPushButton("Generate Report")
        self.generate_button.clicked.connect(self.generate_and_save_report)
        self.sidebar_layout.addWidget(self.generate_button)

        # Settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.show_settings_dialog)
        self.sidebar_layout.addWidget(self.settings_button)

        # Back button to go back to the main menu
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_to_main_menu)
        self.sidebar_layout.addWidget(self.back_button)

        # Add spacer to push any additional items to the bottom
        self.sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def show_settings_dialog(self):
        """Show the settings dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")

        # Layout for the settings dialog
        layout = QVBoxLayout(dialog)

        # "No location" inclusion criteria
        self.no_location_label = QLabel("Enter SR descriptions to include if X,Y = 0,0:")
        self.no_location_input = QLineEdit()
        layout.addWidget(self.no_location_label)
        layout.addWidget(self.no_location_input)

        # OK button to save settings
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.close)  # Properly close the dialog only
        layout.addWidget(ok_button)

        dialog.exec_()  # This keeps the dialog open independently from the main window


    def clear_sidebar(self):
        """Remove all widgets from the sidebar."""
        for i in reversed(range(self.sidebar_layout.count())):
            item = self.sidebar_layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif isinstance(item, QSpacerItem):  # If it's a spacer, remove it
                self.sidebar_layout.removeItem(item)


    def back_to_main_menu(self):
        """Switch back to the main menu in the sidebar."""
        self.create_sidebar_main_menu()
        self.content_area.setCurrentWidget(self.welcome_page)

    def create_welcome_page(self):
        """Create the welcome page view."""
        self.welcome_page = QWidget()
        welcome_layout = QVBoxLayout()
        welcome_label = QLabel("Welcome to the Excel Report Generator!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_label)
        self.welcome_page.setLayout(welcome_layout)
        self.content_area.addWidget(self.welcome_page)

    def create_sr_counter_page(self):
        """Create the SR counter page view."""
        self.sr_counter_page = QWidget()
        sr_counter_layout = QVBoxLayout()

        # Date input fields
        start_date_layout = QHBoxLayout()
        self.start_date_label = QLabel("Start Date:")
        self.start_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_date_input.setCalendarPopup(True)
        start_date_layout.addWidget(self.start_date_label)
        start_date_layout.addWidget(self.start_date_input)
        sr_counter_layout.addLayout(start_date_layout)


        end_date_layout = QHBoxLayout()
        self.end_date_label = QLabel("End Date:")
        self.end_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.end_date_input.setCalendarPopup(True)
        end_date_layout.addWidget(self.end_date_label)
        end_date_layout.addWidget(self.end_date_input)
        sr_counter_layout.addLayout(end_date_layout)

        # Column selection checkboxes (to be filled after loading Excel)
        self.column_groupbox = QGroupBox("Select Columns")
        self.column_layout = QVBoxLayout()
        self.column_groupbox.setLayout(self.column_layout)
        sr_counter_layout.addWidget(self.column_groupbox)

        # Initialize progress bar inside this method
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Add progress bar to the layout
        sr_counter_layout.addWidget(self.progress_bar)

        # Preview button for showing the report preview
        self.preview_button = QPushButton("Preview Report")
        self.preview_button.setStyleSheet("background-color: purple; color: white;")
        self.preview_button.clicked.connect(self.preview_report)
        sr_counter_layout.addWidget(self.preview_button)

        self.sr_counter_page.setLayout(sr_counter_layout)
        self.content_area.addWidget(self.sr_counter_page)

    def show_sr_counter_page(self):
        """Show the SR counter page and change the sidebar."""
        self.create_sidebar_sr_counter()  # Switch the sidebar to SR Counter buttons
        self.content_area.setCurrentWidget(self.sr_counter_page)  # Show the SR Counter content

    def open_file_and_load(self):
        """Open the file dialog to load an Excel file and dynamically generate column checkboxes."""
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
            if file_path:
                self.df = self.load_excel(file_path)
                self.df = self.filter_columns(self.df)
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
            return df
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load Excel file: {e}")
            return None

    def filter_columns(self, df):
        """Filter and rename the required columns in the DataFrame."""
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

    def create_checkboxes(self):
        """Create checkboxes for each column in the loaded Excel file."""
        # Clear existing checkboxes
        for i in reversed(range(self.column_layout.count())):
            widget = self.column_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Create new checkboxes based on the columns in the loaded DataFrame
        if self.df is not None:
            self.column_checkboxes = []
            for col in self.df.columns:
                checkbox = QCheckBox(col)
                checkbox.stateChanged.connect(self.update_selected_columns)
                self.column_layout.addWidget(checkbox)
                self.column_checkboxes.append(checkbox)

    def update_selected_columns(self):
        """Update the list of selected columns based on checkbox states."""
        self.selected_columns = [checkbox.text() for checkbox in self.column_checkboxes if checkbox.isChecked()]

    def generate_and_save_report(self):
        """Generate and save the report based on the selected columns and date range."""
        if self.df is not None and self.selected_columns:
            try:
                start_date = self.start_date_input.dateTime().toPyDateTime()
                end_date = self.end_date_input.dateTime().toPyDateTime()

                if start_date > end_date:
                    QMessageBox.critical(self, "Error", "Start date cannot be after end date")
                    return

                report_df = self.report_generator.generate_report(self.df, start_date, end_date)
                if report_df is not None:
                    output_file = self.report_generator.save_report(report_df)
                    QMessageBox.information(self, "Success", f"Report saved as {output_file}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error generating report: {e}")

    def preview_report(self):
        """Show a preview of the report in a popup window."""
        if self.df is None or not self.selected_columns:
            QMessageBox.warning(self, "No Data", "Please load a file and select columns first.")
            return

        start_date = self.start_date_input.dateTime().toPyDateTime()
        end_date = self.end_date_input.dateTime().toPyDateTime()

        report_df = self.report_generator.generate_report(self.df, start_date, end_date)

        if report_df is None:
            QMessageBox.critical(self, "Error", "Failed to generate the report for preview.")
            return

        # Create a dialog to display the report preview
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("Report Preview")
        preview_layout = QVBoxLayout(preview_dialog)

        table = QTableWidget()
        table.setRowCount(report_df.shape[0])
        table.setColumnCount(report_df.shape[1])
        table.setHorizontalHeaderLabels(report_df.columns)

        # Fill the table with report data
        for i in range(report_df.shape[0]):
            for j in range(report_df.shape[1]):
                table.setItem(i, j, QTableWidgetItem(str(report_df.iloc[i, j])))

        preview_layout.addWidget(table)
        preview_dialog.resize(800, 600)  # Adjust the window size
        preview_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportGeneratorApp()
    window.show()
    sys.exit(app.exec_())
