import pandas as pd
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QLineEdit, QAbstractItemView, QHeaderView
)
from PyQt6.QtCore import Qt
from modules.utils.file_helpers import FileHelper


class EditableTableDialog(QDialog):
    def __init__(self, headers, excel_file_key, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit {headers[0]}")
        self.setMinimumSize(600, 400)

        # Store the headers and file key for loading data
        self.headers = headers
        self.excel_file_key = excel_file_key
        self.data = self.load_data_from_excel()  # Load data on initialization

        # Setup the UI
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Table widget for displaying and editing data
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)

        # Enable autofitting for table columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Load data into the table
        self.load_data()

        # Add search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.search_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)

        # Add buttons
        button_layout = QHBoxLayout()
        add_row_button = QPushButton("Add Row")
        add_row_button.clicked.connect(self.add_row)
        remove_row_button = QPushButton("Remove Selected Row")
        remove_row_button.clicked.connect(self.remove_selected_row)
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes_to_excel)

        button_layout.addWidget(add_row_button)
        button_layout.addWidget(remove_row_button)
        button_layout.addWidget(save_button)

        # Assemble layout
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_data_from_excel(self):
        """Load data from an Excel file using FileHelper."""
        file_path = FileHelper.get_excel_file_path(self.excel_file_key)
        data = FileHelper.read_excel(file_path)

        if data is None:
            print(f"Failed to load data from {file_path}. No data returned.")
            return []
        if not isinstance(data, pd.DataFrame):
            print(f"Unexpected data type: {type(data)}. Expected a pandas DataFrame.")
            return []

        # Convert DataFrame rows to tuples for insertion into the table
        return [tuple(row) for row in data.values]

    def load_data(self):
        """Load initial data into the table."""
        self.table.setRowCount(len(self.data))
        for row, item in enumerate(self.data):
            for col, value in enumerate(item):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def search_table(self):
        """Filter rows based on search query."""
        query = self.search_box.text().lower()
        for row in range(self.table.rowCount()):
            matches = any(
                query in (self.table.item(row, col).text() or "").lower()
                for col in range(self.table.columnCount())
            )
            self.table.setRowHidden(row, not matches)

    def add_row(self):
        """Add a new, blank row to the table."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

    def remove_selected_row(self):
        """Remove the currently selected row."""
        current_row = self.table.currentRow()
        if current_row != -1:
            self.table.removeRow(current_row)

    def save_changes_to_excel(self):
        """Save table data back to the original Excel file."""
        file_path = FileHelper.get_excel_file_path(self.excel_file_key)
        data_to_save = []

        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                value = item.text().strip() if item else ""  # Handle empty cells
                row_data.append(value)
            data_to_save.append(row_data)

        # Convert data to a DataFrame
        df = pd.DataFrame(data_to_save, columns=self.headers)
        # print(f"DataFrame to save:\n{df}")  # Debugging: Print the DataFrame before saving

        try:
            # Save the DataFrame to Excel
            df.to_excel(file_path, index=False, engine="openpyxl")
            print(f"Data successfully saved to {file_path}")
        except Exception as e:
            print(f"Error saving data: {e}")




