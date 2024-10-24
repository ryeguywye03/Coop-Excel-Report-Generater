# from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
# from PyQt5.QtCore import Qt

# class ReportPreview(QDialog):
#     def __init__(self, parent, report_df):
#         super().__init__(parent)
#         self.setWindowTitle("Report Preview")
#         self.resize(1200, 600)  # Adjust the window size as needed
#         self.setup_ui(report_df)

#     def setup_ui(self, report_df):
#         """Setup the UI and populate it with DataFrame content."""
#         layout = QVBoxLayout(self)

#         # Table to display report data
#         table = QTableWidget()
#         table.setRowCount(report_df.shape[0])
#         table.setColumnCount(report_df.shape[1])
#         table.setHorizontalHeaderLabels(report_df.columns.tolist())

#         # Enable horizontal and vertical scrollbars
#         table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
#         table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

#         # Allow columns to stretch and fill the space
#         table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

#         # Fill the table with report data
#         for i in range(report_df.shape[0]):
#             for j in range(report_df.shape[1]):
#                 table.setItem(i, j, QTableWidgetItem(str(report_df.iloc[i, j])))

#         # Set the table to expand when resizing the window
#         table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

#         layout.addWidget(table)
#         self.setLayout(layout)
