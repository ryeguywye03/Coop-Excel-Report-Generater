import pandas as pd
from logic.logger_manager import LoggerManager  # Import the logger
import os
from datetime import datetime

class SRReportGenerator:
    def __init__(self, progress_bar):
        self.progress_bar = progress_bar
        self.logger = LoggerManager()  # Initialize logger
        self.logger.log_info("SRReportGenerator initialized")

    def generate_report(self, df: pd.DataFrame, selected_columns, start_date: datetime, end_date: datetime, sort_by=None, exclusions=None):
        """Generate the report by processing the DataFrame within the start and end date range, grouped by selected columns, and sort it."""

        self.logger.log_info(f"Starting report generation: {start_date} to {end_date}")
        try:
            # Exclude SR Type and Group based on the settings
            if exclusions:
                if exclusions['excluded_sr_type']:
                    self.logger.log_info(f"Excluding SR Type: {exclusions['excluded_sr_type']}")
                    df = df[df['Type Description'] != exclusions['excluded_sr_type']]
                if exclusions['excluded_group']:
                    self.logger.log_info(f"Excluding Group: {exclusions['excluded_group']}")
                    df = df[df['Group Description'] != exclusions['excluded_group']]

            # Ensure 'Created Date' is properly handled and convert to datetime if selected
            df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
            df = df.dropna(subset=['Created Date'])
            df = df[(df['Created Date'] >= start_date) & (df['Created Date'] <= end_date)]

            # Extract the month from 'Created Date'
            df['Month'] = df['Created Date'].dt.month  # Extract month

            # Define month names
            all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            # Filter the months based on the user-defined date range
            start_month = start_date.month
            end_month = end_date.month

            # Dynamically include only the months within the date range
            included_months = all_months[start_month - 1:end_month]

            # Initialize combined data and grand totals
            combined_data = []
            grand_totals = {month: 0 for month in included_months}
            grand_totals['TOTAL'] = 0

            # Group data by the selected columns
            grouped = df.groupby(selected_columns)
            group_count = len(grouped)

            for group_values, group_data in grouped:
                # Monthly counts
                monthly_counts = [
                    group_data[group_data['Month'] == month].shape[0]
                    for month in range(start_month, end_month + 1)
                ]

                total_count = sum(monthly_counts)

                # Create row data for each group
                row_data = {col: value for col, value in zip(selected_columns, group_values)}
                row_data.update({
                    **dict(zip(included_months, monthly_counts)),
                    'TOTAL': total_count
                })
                combined_data.append(row_data)

                # Update grand totals
                for month_name, count in zip(included_months, monthly_counts):
                    grand_totals[month_name] += count
                grand_totals['TOTAL'] += total_count

                # Update progress bar
                progress = int(len(combined_data) / max(group_count, 1) * 100)
                self.progress_bar.setValue(progress)

            # Create DataFrame for the report
            columns_order = selected_columns + included_months + ['TOTAL']
            combined_report = pd.DataFrame(combined_data)[columns_order]

            # Sort the report by the selected field, if applicable
            if sort_by and sort_by in combined_report.columns:
                self.logger.log_info(f"Sorting report by {sort_by}")
                combined_report = combined_report.sort_values(by=sort_by)

            # Append grand totals row **after sorting**, so it's at the bottom
            total_row = {col: '' for col in selected_columns}
            total_row.update(grand_totals)
            combined_report = pd.concat([combined_report, pd.DataFrame([total_row])], ignore_index=True)

            # Set progress bar to 100% when done
            self.progress_bar.setValue(100)

            self.logger.log_info("Report generation completed")
            return combined_report

        except Exception as e:
            self.logger.log_error(f"Error during report generation: {e}")
            return None

    def show_report_preview(self, preview_df):
        """Display a preview of the report in a QDialog."""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem

        self.logger.log_info("Displaying report preview")
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Report Preview")
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
            dialog.exec_()  # Open dialog in modal form

        except Exception as e:
            self.logger.log_error(f"Error displaying report preview: {e}")

    def save_report(self, report_df):
        """Save the generated report to an Excel file with formatting."""
        try:
            self.logger.log_info("Saving report to Excel file")
            directory = os.path.expanduser("~/Desktop")
            base_filename = "report_"
            file_number = 1
            while os.path.exists(os.path.join(directory, f"{base_filename}{file_number:03}.xlsx")):
                file_number += 1

            output_file = os.path.join(directory, f"{base_filename}{file_number:03}.xlsx")

            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                report_df.to_excel(writer, sheet_name='Report', index=False)

                # Access the workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets['Report']

                # Apply autofit column width to all columns and set specific widths for month columns
                for idx, col in enumerate(report_df.columns):
                    if col in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                        worksheet.set_column(idx, idx, 12)  # Set width for month columns to 12
                    else:
                        max_len = max(
                            report_df[col].astype(str).map(len).max(),  # Maximum content length
                            len(col)  # Column header length
                        ) + 2
                        worksheet.set_column(idx, idx, max_len)  # Autofit based on content

                # Format the header: bold, background color
                header_format = workbook.add_format({'bold': True, 'bg_color': '#D9EAD3', 'align': 'center'})
                for col_num, value in enumerate(report_df.columns):
                    worksheet.write(0, col_num, value, header_format)

                # Bold the 'Total' row if needed
                total_format = workbook.add_format({'bold': True})
                worksheet.write(f'A{len(report_df)+1}', 'Total', total_format)  # Assuming 'Total' row is at the end

            self.logger.log_info(f"Report saved at {output_file}")
            return output_file

        except Exception as e:
            self.logger.log_error(f"Failed to save report: {e}")
            return None
