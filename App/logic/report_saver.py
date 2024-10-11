import os
import pandas as pd

class ReportSaver:
    def save_report(self, report_df):
        """Save the generated report to an Excel file with autofit column widths."""
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

                # Set column widths based on the max length of the data in each column
                for idx, col in enumerate(report_df.columns):
                    max_len = max(
                        report_df[col].astype(str).map(len).max(),  # Maximum content length in the column
                        len(str(col))  # Length of the column name
                    ) + 2  # Adding a little extra padding
                    worksheet.set_column(idx, idx, max_len)

                return output_file
        except Exception as e:
            print(f"Failed to save report: {e}")
            return None
