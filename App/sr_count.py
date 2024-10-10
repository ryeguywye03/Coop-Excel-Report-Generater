import pandas as pd
from PyQt5.QtWidgets import QProgressBar
from datetime import datetime

class SRReportGenerator:
    def __init__(self, progress_bar: QProgressBar):
        self.progress_bar = progress_bar

    def generate_report(self, df, start_date: datetime, end_date: datetime):
        """Generate the report by processing the DataFrame within the start and end date range, grouped by SR GROUP."""

        # Convert 'Created Date' to datetime and filter based on the provided date range
        df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
        df = df.dropna(subset=['Created Date'])
        df = df[(df['Created Date'] >= start_date) & (df['Created Date'] <= end_date)]

        # Extract the month from 'Created Date'
        df['Month'] = df['Created Date'].dt.month

        # Define month names
        all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        start_month = start_date.month
        end_month = end_date.month
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
            self.progress_bar.setValue(self.progress_bar.value() + int(100 / max(group_count, 1)))

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
