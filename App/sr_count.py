import pandas as pd
import os
from datetime import datetime
from PyQt5.QtWidgets import QProgressBar, QMessageBox

class SRReportGenerator:
    def __init__(self, progress_bar: QProgressBar):
        self.progress_bar = progress_bar

    def generate_report(self, df: pd.DataFrame, start_date: datetime, end_date: datetime):
        """Generate the report by processing the DataFrame within the start and end date range."""
        # Convert 'Created Date' to datetime and filter based on the provided date range
        df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
        df = df.dropna(subset=['Created Date'])
        df = df[(df['Created Date'] >= start_date) & (df['Created Date'] <= end_date)]

        # Extract the month from 'Created Date'
        df['Month'] = df['Created Date'].dt.month

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

        # Group data by 'Group Description' and 'Type Description' (SR Group and SR Type)
        grouped = df.groupby(['Group Description', 'Type Description'])
        group_count = len(grouped)

        # Process each group and calculate monthly totals for only the months in the specified range
        for (group_descr, type_descr), group_data in grouped:
            monthly_counts = [
                group_data[group_data['Month'] == month].shape[0]
                for month in range(start_month, end_month + 1)
            ]
            total_count = sum(monthly_counts)

            # Create row data for each SR GROUP and SR TYPE combination
            row_data = {
                'SR TYPE': type_descr,
                'Group Description': group_descr,
                **dict(zip(included_months, monthly_counts)),
                'TOTAL': total_count
            }
            combined_data.append(row_data)

            # Update grand totals
            for month_name, count in zip(included_months, monthly_counts):
                grand_totals[month_name] += count
            grand_totals['TOTAL'] += total_count

            # Update progress bar
            progress = int(len(combined_data) / max(group_count, 1) * 100)
            self.progress_bar.setValue(progress)

        # Append grand totals row to the report
        total_row = {
            'SR TYPE': 'Total',
            'Group Description': '',
            **grand_totals
        }
        combined_data.append(total_row)

        # Create a DataFrame for the report
        columns_order = ['SR TYPE', 'Group Description'] + included_months + ['TOTAL']
        combined_report = pd.DataFrame(combined_data)[columns_order]

        # Set progress bar to 100% when done
        self.progress_bar.setValue(100)

        return combined_report

    def save_report(self, report_df: pd.DataFrame):
        """Save the generated report to an Excel file with manual column width adjustment."""
        try:
            directory = os.path.expanduser("~/Desktop")
            base_filename = "report_"
            file_number = 1
            while os.path.exists(os.path.join(directory, f"{base_filename}{file_number:03}.xlsx")):
                file_number += 1

            output_file = os.path.join(directory, f"{base_filename}{file_number:03}.xlsx")

            # Write the report to Excel
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                report_df.to_excel(writer, sheet_name='Report', index=False)

                # Get workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets['Report']

                # Calculate and set column widths based on the length of the content
                for i, col in enumerate(report_df.columns):
                    max_len = max(
                        report_df[col].astype(str).map(len).max(),  # Max length of column values
                        len(str(col))  # Length of the column header
                    )
                    worksheet.set_column(i, i, max_len + 2)  # Add padding for better appearance

                # Apply header format
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#D7E4BC',
                    'border': 1
                })

                for col_num, value in enumerate(report_df.columns.values):
                    worksheet.write(0, col_num, value, header_format)

            return output_file

        except Exception as e:
            raise Exception(f"Failed to save report: {e}")

