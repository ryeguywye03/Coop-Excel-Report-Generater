from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDateTimeEdit, QCheckBox, QProgressBar, QFileDialog, QMessageBox, QScrollArea, QGroupBox, QPushButton
from PyQt5.QtCore import QDateTime
import pandas as pd
from logic.sr_count import SRReportGenerator
from ui.report_preview import ReportPreview  # Import the ReportPreview dialog


class SRCounterUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui(parent)

    def setup_ui(self, parent):
        self.main_layout = QVBoxLayout(self)

        # Sidebar with a "Back to Main Menu" button
        sidebar_group = self.setup_sidebar(parent)

        # Main panel for SR counter options
        sr_counter_panel = self.setup_main_panel()

        # Add sidebar and SR Counter panel to main layout
        self.main_layout.addWidget(sidebar_group)
        self.main_layout.addWidget(sr_counter_panel)

    def setup_sidebar(self, parent):
        """Set up the sidebar for the SR Counter page."""
        sidebar_group = QGroupBox("SR Counter Options")
        sidebar_layout = QVBoxLayout()

        # Button to go back to the main menu
        back_to_menu_button = QPushButton("Back to Main Menu")
        back_to_menu_button.clicked.connect(parent.switch_to_main_menu)

        sidebar_layout.addWidget(back_to_menu_button)

        sidebar_group.setLayout(sidebar_layout)
        return sidebar_group

    def setup_main_panel(self):
        """Set up the main content area for SR Counter UI."""
        main_panel_group = QGroupBox("SR Counter")
        main_panel_layout = QVBoxLayout()

        # Date range inputs
        date_layout = QHBoxLayout()
        start_date_label = QLabel("Start Date:")
        self.start_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_date_input.setCalendarPopup(True)
        end_date_label = QLabel("End Date:")
        self.end_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.end_date_input.setCalendarPopup(True)

        date_layout.addWidget(start_date_label)
        date_layout.addWidget(self.start_date_input)
        date_layout.addWidget(end_date_label)
        date_layout.addWidget(self.end_date_input)

        # Add column selection checkboxes
        columns_group = QGroupBox("Select Columns")
        columns_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Add checkboxes
        self.checkboxes = []
        for column in ["Service Request Number", "Created Date", "Type Description", "Group Description"]:
            checkbox = QCheckBox(column)
            scroll_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        scroll_area.setWidget(scroll_content)
        columns_layout.addWidget(scroll_area)
        columns_group.setLayout(columns_layout)

        # Add the progress bar and buttons for generating reports
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        button_layout = QHBoxLayout()
        preview_button = QPushButton("Preview Report")
        generate_button = QPushButton("Generate Report")

        button_layout.addWidget(preview_button)
        button_layout.addWidget(generate_button)

        # Add all elements to the main panel layout
        main_panel_layout.addLayout(date_layout)
        main_panel_layout.addWidget(columns_group)
        main_panel_layout.addWidget(self.progress_bar)
        main_panel_layout.addLayout(button_layout)

        main_panel_group.setLayout(main_panel_layout)
        return main_panel_group

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

    def generate_report(self):
        """Generate and save the report based on the selected columns and date range."""
        if self.df is not None:
            selected_columns = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]

            if not selected_columns:
                QMessageBox.warning(self, "Warning", "No columns selected for the report.")
                return

            try:
                start_date = self.start_date_input.dateTime().toPyDateTime()
                end_date = self.end_date_input.dateTime().toPyDateTime()

                if start_date > end_date:
                    QMessageBox.critical(self, "Error", "Start date cannot be after end date")
                    return

                # Call the report generator from sr_count.py
                report_df = self.report_generator.generate_report(self.df, selected_columns, start_date, end_date)

                # Save the report
                output_file = self.save_report(report_df)
                if output_file:
                    QMessageBox.information(self, "Success", f"Report saved as {output_file}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error generating report: {e}")

    def preview_report(self):
        """Show a preview of the report by calling the ReportPreview dialog."""
        if self.df is None or not self.checkboxes:
            QMessageBox.warning(self, "No Data", "Please load a file and select columns first.")
            return

        selected_columns = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        if not selected_columns:
            QMessageBox.warning(self, "Warning", "No columns selected for the preview.")
            return

        try:
            start_date = self.start_date_input.dateTime().toPyDateTime()
            end_date = self.end_date_input.dateTime().toPyDateTime()

            if start_date > end_date:
                QMessageBox.critical(self, "Error", "Start date cannot be after end date")
                return

            # Call the generate_report function to filter and generate the report DataFrame
            sr_report_generator = SRReportGenerator(self.progress_bar, self)
            report_df = sr_report_generator.generate_report(self.df, selected_columns, start_date, end_date)

            # Call the ReportPreview dialog (from report_preview.py) to display the report
            if report_df is not None:
                dialog = ReportPreview(self, report_df)
                dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating preview: {e}")



    def save_report(self, report_df):
        """Save the generated report to an Excel file."""
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Report As", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
            if file_path:
                report_df.to_excel(file_path, index=False)  # Save DataFrame to Excel file
                return file_path
            else:
                QMessageBox.warning(self, "Warning", "No file selected for saving the report.")
                return None
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save report: {e}")
            return None
