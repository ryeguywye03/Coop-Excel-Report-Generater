import pandas as pd
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from modules.utils.file_helpers import FileHelper  # Import FileHelper to use the existing read_excel method

class FileLoader:
    def __init__(self, parent):
        self.parent = parent
        self.df = None

    def load_file(self):
        """Loads the Excel file and updates the columns."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(self.parent, "Open Excel File", "", "Excel Files (*.xlsx *.xls);;All Files (*)")
            if file_path:
                self.df = FileHelper.read_excel(file_path)  # Use FileHelper to load the file
                if self.df is not None:
                    # Map columns and check for missing required columns
                    self.df = self.map_columns(self.df)
                    self.check_missing_columns(self.df)
                    self.parent.checkbox_manager.populate_checkboxes(self.df.columns)
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Failed to load Excel file: {e}")

    def check_missing_columns(self, df):
        """Check if there are any missing required columns."""
        required_columns = ["Service Request Number", "Created Date", "Type Description", "Group Description", "X Value", "Y Value"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            QMessageBox.warning(self.parent, "Warning", f"The following required columns are missing: {', '.join(missing_columns)}")

    def map_columns(self, df):
        """Map known Excel columns to user-friendly names."""
        column_mapping = {
            'Service_Re': 'Service Request Number',
            'Created_Da': 'Created Date',
            'Type_Descr': 'Type Description',
            'Group_Desc': 'Group Description',
            'X_Value': 'X Value',
            'Y_Value': 'Y Value'
        }

        # Apply column mapping to DataFrame
        df = df.rename(columns=column_mapping)
        return df
