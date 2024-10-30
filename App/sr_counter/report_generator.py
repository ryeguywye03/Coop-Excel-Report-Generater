import pandas as pd
from utils.logger_manager import LoggerManager
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, progress_bar):
        self.progress_bar = progress_bar
        self.logger = LoggerManager()  # Initialize logger
        self.logger.log_info("ReportGenerator initialized")
        self.included_months = []  # Initialize as an instance variable

    def generate_report(self, df: pd.DataFrame, selected_columns, start_date: datetime, end_date: datetime, sort_by=None, exclusions=None):
        """Generate the report by processing the DataFrame within the start and end date range, grouped by selected columns, and sorted if specified."""
        
        self.logger.log_info(f"Starting report generation from {start_date} to {end_date}")
        self.logger.log_debug(f"Selected columns for grouping: {selected_columns}")
        self.logger.log_debug(f"Sorting by column: {sort_by}")
        
        try:
            # Apply exclusions
            if exclusions:
                self.logger.log_info("Applying exclusions")
                if exclusions['excluded_sr_type']:
                    df = df[~df['Type Description'].isin(exclusions['excluded_sr_type'])]
                    self.logger.log_debug(f"Excluded SR Types: {exclusions['excluded_sr_type']}")
                
                if exclusions['excluded_group']:
                    df = df[~df['Group Description'].isin(exclusions['excluded_group'])]
                    self.logger.log_debug(f"Excluded Groups: {exclusions['excluded_group']}")

                # Handle no location exclusions
                if exclusions['no_location_excluded_sr_type'] or exclusions['no_location_excluded_group']:
                    no_location_df = df[(df['X Value'] == 0) & (df['Y Value'] == 0)]
                    if exclusions['no_location_excluded_sr_type']:
                        no_location_df = no_location_df[~no_location_df['Type Description'].isin(exclusions['no_location_excluded_sr_type'])]
                    if exclusions['no_location_excluded_group']:
                        no_location_df = no_location_df[~no_location_df['Group Description'].isin(exclusions['no_location_excluded_group'])]
                    df = pd.concat([df[~((df['X Value'] == 0) & (df['Y Value'] == 0))], no_location_df])

            # Date filtering
            df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
            df = df.dropna(subset=['Created Date'])
            df = df[(df['Created Date'] >= start_date) & (df['Created Date'] <= end_date)]
            df['Month'] = df['Created Date'].dt.month

            # Define months to include
            all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            self.included_months = all_months[start_date.month - 1:end_date.month]  # Set as an instance variable

            combined_data = []
            grand_totals = {month: 0 for month in self.included_months}
            grand_totals['TOTAL'] = 0

            # Grouping
            valid_columns = [col for col in selected_columns if col in df.columns]
            if not valid_columns:
                self.logger.log_error("No valid columns selected for grouping.")
                QMessageBox.critical(None, "Error", "No valid columns selected for grouping.")
                return None

            grouped = df.groupby(valid_columns)

            # Process each group
            for group_values, group_data in grouped:
                monthly_counts = [group_data[group_data['Month'] == month].shape[0] for month in range(start_date.month, end_date.month + 1)]
                total_count = sum(monthly_counts)
                row_data = {col: value for col, value in zip(selected_columns, group_values)}
                row_data.update({**dict(zip(self.included_months, monthly_counts)), 'TOTAL': total_count})
                combined_data.append(row_data)

                for month_name, count in zip(self.included_months, monthly_counts):
                    grand_totals[month_name] += count
                grand_totals['TOTAL'] += total_count

                # Update progress bar
                progress = int(len(combined_data) / max(len(grouped), 1) * 100)
                self.progress_bar.setValue(progress)

            # Create DataFrame for combined data
            combined_report = pd.DataFrame(combined_data)
            combined_report = combined_report[valid_columns + self.included_months + ['TOTAL']]

            # Sorting
            if sort_by and sort_by in combined_report.columns:
                combined_report = combined_report.sort_values(by=sort_by)
                self.logger.log_info(f"Sorted by {sort_by}")

            # Append totals row only once
            total_row = {col: '' for col in selected_columns}
            total_row.update(grand_totals)
            combined_report = pd.concat([combined_report, pd.DataFrame([total_row])], ignore_index=True)

            self.logger.log_info("Report generation completed")
            return combined_report

        except Exception as e:
            self.logger.log_error(f"Error during report generation: {e}")
            return None

    def show_report_preview(self, preview_df):
        """Display a preview of the report in a QDialog."""
        self.logger.log_info("Displaying report preview")
        try:
            dialog = QDialog()
            dialog.setWindowTitle("Report Preview")
            dialog.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint)  # Enable maximize button
            layout = QVBoxLayout(dialog)

            # Create table widget
            table = QTableWidget()
            table.setRowCount(preview_df.shape[0])
            table.setColumnCount(preview_df.shape[1])
            table.setHorizontalHeaderLabels(preview_df.columns)

            # Fill the table with preview data
            for i in range(preview_df.shape[0]):
                for j in range(preview_df.shape[1]):
                    table.setItem(i, j, QTableWidgetItem(str(preview_df.iloc[i, j])))

            layout.addWidget(table)
            dialog.setLayout(layout)
            dialog.resize(800, 400)  # Set dialog size
            table.resizeColumnsToContents()

            dialog.exec()

        except Exception as e:
            self.logger.log_error(f"Error displaying report preview: {e}")

    def save_report(self, report_df):
        """Save the generated report to an Excel file with enhanced formatting."""
        try:
            self.logger.log_info("Saving report to Excel file")

            # Generate default filename with the required format
            current_time = datetime.now()
            default_filename = current_time.strftime("sr_count_report-%m-%d-%Y-%H-%M-%S.xlsx")

            # Prompt for file location with default filename
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Save Report",
                os.path.join(os.path.expanduser("~/Desktop"), default_filename),
                "Excel Files (*.xlsx)"
            )

            if not file_path:
                self.logger.log_info("Save canceled by user.")
                return None

            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                report_df.to_excel(writer, sheet_name='Report', index=False)
                workbook = writer.book
                worksheet = writer.sheets['Report']

                # Define formats
                header_format = workbook.add_format({
                    'bold': True,
                    'font_color': 'white',
                    'bg_color': '#4F81BD',
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter'
                })

                cell_format = workbook.add_format({
                    'border': 1,
                    'align': 'left',
                    'valign': 'vcenter'
                })

                total_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#D9EAD3',
                    'border': 1,
                    'align': 'center'
                })

                vertical_total_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#D9EAD3',
                    'border': 1,
                    'align': 'center'
                })

                # Apply header format
                for col_num, value in enumerate(report_df.columns):
                    worksheet.write(0, col_num, value, header_format)

                # Set all cells format except header
                worksheet.set_column(0, len(report_df.columns) - 1, 15, cell_format)

                # Apply total format to the last row
                total_row_idx = len(report_df) - 1
                for col_num in range(len(report_df.columns)):
                    # Check if the column is in included_months or TOTAL, and apply the vertical total format
                    if report_df.columns[col_num] in self.included_months or report_df.columns[col_num] == 'TOTAL':
                        worksheet.write(total_row_idx, col_num, report_df.iloc[total_row_idx, col_num], vertical_total_format)
                    else:
                        worksheet.write(total_row_idx, col_num, report_df.iloc[total_row_idx, col_num], total_format)

            self.logger.log_info(f"Report saved at {file_path}")
            return file_path

        except Exception as e:
            self.logger.log_error(f"Failed to save report: {e}")
            return None
