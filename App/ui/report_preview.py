from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem

class ReportPreview(QDialog):
    def __init__(self, parent, report_df):
        super().__init__(parent)
        self.setWindowTitle("Report Preview")
        self.setup_ui(report_df)

    def setup_ui(self, report_df):
        """Setup the UI and populate it with DataFrame content."""
        layout = QGridLayout(self)

        self.resize(1200, 600)

        # Table to display report data
        table = QTableWidget()
        table.setRowCount(report_df.shape[0])
        table.setColumnCount(report_df.shape[1])
        table.setHorizontalHeaderLabels(report_df.columns.tolist())

        # Fill the table with report data
        for i in range(report_df.shape[0]):
            for j in range(report_df.shape[1]):
                table.setItem(i, j, QTableWidgetItem(str(report_df.iloc[i, j])))

        layout.addWidget(table, 0, 0, 1, 2)
