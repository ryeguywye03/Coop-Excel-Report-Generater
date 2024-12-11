import pandas as pd
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from modules.utils.file_helpers import FileHelper  # Import FileHelper to use read_excel and read_csv methods

class FileLoader:
    def __init__(self, parent):
        self.parent = parent
        self.df = None

    def load_file(self):
        """
        Loads an Excel or CSV file using a file dialog and updates the columns.
        """
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self.parent,
                "Open File",
                "",
                "Supported Files (*.xlsx *.xls *.csv);;Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*)"
            )
            if file_path:
                # Use FileHelper to read the file
                self.df = FileHelper.read_file(file_path)

                if self.df is not None:
                    # Map columns and check for missing required columns
                    self.df = self.map_columns(self.df)
                    self.check_missing_columns(self.df)

                    # Populate UI checkboxes with column names
                    self.parent.checkbox_manager.populate_checkboxes(self.df.columns)
                else:
                    QMessageBox.warning(self.parent, "Error", "The selected file could not be read.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Failed to load file: {e}")

    def check_missing_columns(self, df):
        """
        Check if there are any missing required columns.
        """
        required_columns = {
            "Service Request Number": ["Service Request Number", "Service_Re"],
            "Created Date": ["Created Date", "Created_Da", "Created Date Only"],
            "Type Description": ["Type Description", "Type_Descr"],
            "Group Description": ["Group Description", "Group_Desc"],
            "X Value": ["X Value", "X_Value"],
            "Y Value": ["Y Value", "Y_Value"]
        }

        # Identify missing columns based on alternatives
        missing_columns = [
            key for key, options in required_columns.items()
            if not any(col in df.columns for col in options)
        ]

        if missing_columns:
            QMessageBox.warning(
                self.parent,
                "Missing Columns",
                f"The following required columns are missing: {', '.join(missing_columns)}"
            )

    def map_columns(self, df):
        """
        Map known columns with alternative names to user-friendly names.
        """
        column_mapping = {
            "Service Request Number": ["Service Request Number", "Service_Re","SR #"],
            "Created Date": ["Created Date", "Created_Da", "Created Date Only"],
            "Type Description": ["Type Description", "Type_Descr"],
            "Group Description": ["Group Description", "Group_Desc"],
            "X Value": ["X Value", "X_Value"],
            "Y Value": ["Y Value", "Y_Value"]
        }

        for friendly_name, options in column_mapping.items():
            for option in options:
                if option in df.columns:
                    df = df.rename(columns={option: friendly_name})
                    break  # Stop renaming once a match is found

        return df

    def validate_time_columns(self):
        """
        Validate if the file contains time-related data.
        """
        if self.df is None:
            QMessageBox.warning(self.parent, "No Data", "No file loaded to validate.")
            return False

        if "Created Date" in self.df.columns:
            # Check for valid datetime in the "Created Date" column
            if not pd.to_datetime(self.df["Created Date"], errors="coerce").isnull().all():
                return True

        elif "Time" in self.df.columns:
            # Check for valid time in a standalone "Time" column
            if not pd.to_datetime(self.df["Time"], errors="coerce").isnull().all():
                return True

        QMessageBox.warning(
            self.parent,
            "No Time Data",
            "The file does not contain valid time-related data."
        )
        return False

    def filter_by_time_frame(self, start_date, end_date, start_time=None, end_time=None):
        """
        Filter the DataFrame by the specified time frame and date range.
        """
        if self.df is None:
            QMessageBox.warning(self.parent, "No Data", "No file loaded to filter.")
            return None

        if not self.validate_time_columns():
            return self.df

        if "Created Date" in self.df.columns:
            self.df["Created Date"] = pd.to_datetime(self.df["Created Date"], errors="coerce")
            # Filter by date range
            self.df = self.df[(self.df["Created Date"].dt.date >= start_date) &
                              (self.df["Created Date"].dt.date <= end_date)]

            # Filter by time frame if provided
            if start_time and end_time:
                self.df = self.df[(self.df["Created Date"].dt.time >= start_time) &
                                  (self.df["Created Date"].dt.time <= end_time)]

        elif "Time" in self.df.columns:
            self.df["Time"] = pd.to_datetime(self.df["Time"], errors="coerce").dt.time
            if start_time and end_time:
                self.df = self.df[(self.df["Time"] >= start_time) & (self.df["Time"] <= end_time)]

        return self.df
