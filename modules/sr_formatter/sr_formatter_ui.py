import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QPushButton, QLabel, QGridLayout, QHBoxLayout,
    QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QDialog
)
from PyQt6.QtCore import Qt
from modules.utils.logger_manager import LoggerManager
from modules.sr_formatter import SRFormatter


class SRFormatterUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent

        # Initialize logger
        self.logger = LoggerManager()

        # Initialize SRFormatter backend
        self.sr_formatter = SRFormatter(logger=self.logger)

        # Setup UI
        self.setup_ui()

        # Variables to store file paths
        self.input_file = None

    def setup_ui(self):
        """Set up the UI layout."""
        self.setObjectName("mainPanel")  # Main panel object name
        self.main_layout = QGridLayout(self)

        # Set up the sidebar and main panel
        sidebar = self.setup_sidebar()
        formatter_panel = self.setup_main_panel()

        self.main_layout.addWidget(sidebar, 0, 0, 1, 1)
        self.main_layout.addWidget(formatter_panel, 0, 1, 1, 2)

    def setup_sidebar(self):
        """Set up the sidebar for SR Formatter."""
        sidebar_group = QGroupBox("SR Formatter Options")
        sidebar_group.setObjectName("sidebarGroup")
        sidebar_layout = QVBoxLayout()

        # Load Input File Button
        load_excel_button = QPushButton("Load Input File")
        load_excel_button.setProperty("class", "sidebar-button")
        load_excel_button.clicked.connect(self.load_input_file)

        # Back to Main Menu Button
        back_button = QPushButton("Back to Main Menu")
        back_button.setProperty("class", "sidebar-button")
        back_button.clicked.connect(self.main_window.switch_to_main_menu)

        # Add buttons to the layout
        sidebar_layout.addWidget(load_excel_button)
        sidebar_layout.addStretch(1)
        sidebar_layout.addWidget(back_button)

        sidebar_group.setLayout(sidebar_layout)
        return sidebar_group

    def setup_main_panel(self):
        """Set up the main content area for SR Formatter."""
        formatter_group = QGroupBox("SR Formatter")
        formatter_group.setObjectName("formatterGroup")
        main_panel_layout = QVBoxLayout()

        # Input Label
        self.input_label = QLabel("Input File: Not Selected")
        self.input_label.setProperty("class", "label")

        # Buttons for Preview and Format
        button_layout = QHBoxLayout()

        preview_button = QPushButton("Preview")
        preview_button.setProperty("class", "report-button")
        preview_button.clicked.connect(self.preview_file)

        format_button = QPushButton("Format and Save")
        format_button.setProperty("class", "report-button")
        format_button.clicked.connect(self.format_and_save)

        button_layout.addWidget(preview_button)
        button_layout.addWidget(format_button)

        # Add widgets to the layout
        main_panel_layout.addWidget(self.input_label)
        main_panel_layout.addLayout(button_layout)

        formatter_group.setLayout(main_panel_layout)
        return formatter_group

    def load_input_file(self):
        """Load the input file."""
        input_file, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "Excel or CSV Files (*.xlsx *.csv)")
        if input_file:
            self.input_label.setText(f"Input File: {input_file}")
            self.input_file = input_file

    def preview_file(self):
        """Preview the formatted data."""
        if not self.input_file:
            QMessageBox.warning(self, "No Input File", "Please load an input file first.")
            return

        try:
            # Generate preview using SRFormatter
            df_preview = self.sr_formatter.preview_sr_data(self.input_file)

            # Display the preview in a dialog
            self.show_preview_dialog(df_preview)
        except KeyError as ke:
            self.logger.log_error(f"KeyError during preview: {ke}")
            QMessageBox.warning(self, "Invalid File", f"Error in the file: {ke}")
        except Exception as e:
            self.logger.log_error(f"Error previewing file: {e}")
            QMessageBox.critical(self, "Error", f"Failed to preview the file. Details:\n{e}")

    def format_and_save(self):
        """Format the SR file and save it."""
        if not self.input_file:
            QMessageBox.warning(self, "No Input File", "Please load an input file first.")
            return

        try:
            # Format and save the file using SRFormatter
            file_path = self.sr_formatter.format_sr_data(self.input_file)
            QMessageBox.information(self, "Success", f"Formatted data saved to {file_path}")
        except Exception as e:
            self.logger.log_error(f"Error formatting and saving file: {e}")
            QMessageBox.critical(self, "Error", f"Failed to format and save the file. Details:\n{e}")

    def show_preview_dialog(self, df):
        """Display a dialog to preview the DataFrame."""
        try:
            dialog = QDialog()
            dialog.setWindowTitle("Preview SR Data")
            dialog.resize(800, 600)

            layout = QVBoxLayout(dialog)
            table = QTableWidget()
            table.setRowCount(df.shape[0])
            table.setColumnCount(df.shape[1])
            table.setHorizontalHeaderLabels(df.columns)

            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

            layout.addWidget(table)
            dialog.setLayout(layout)
            dialog.exec()
        except Exception as e:
            self.logger.log_error(f"Error displaying preview dialog: {e}")
