import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QPushButton
from ui.main_menu import MainMenuUI
from ui.sr_counter_ui import SRCounterUI
import os

class ReportGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup the main window and central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout(self.central_widget)

        # Sidebar and main panel containers
        self.sidebar = QWidget()  # Sidebar container
        self.main_panel = QStackedWidget()  # Main panel container

        # Add sidebar and main panel to layout
        self.main_layout.addWidget(self.sidebar, 0, 0, 1, 1)
        self.main_layout.addWidget(self.main_panel, 0, 1, 1, 2)

        # Initialize the Main Menu and SR Counter pages
        self.main_menu_page = MainMenuUI(self)
        self.sr_counter_page = SRCounterUI(self)

        # Add both to the main panel stack
        self.main_panel.addWidget(self.main_menu_page)
        self.main_panel.addWidget(self.sr_counter_page)

        self.setMinimumSize(1000, 600)

        # Default page is the Main Menu
        self.switch_to_main_menu()

    def switch_to_main_menu(self):
        """Switch to the Main Menu page."""
        self.main_panel.setCurrentWidget(self.main_menu_page)
        self.setup_main_menu_sidebar()  # Setup the sidebar for the Main Menu

    def switch_to_sr_counter(self):
        """Switch to the SR Counter page."""
        self.main_panel.setCurrentWidget(self.sr_counter_page)
        self.setup_sr_counter_sidebar()  # Setup the sidebar for SR Counter

    def setup_main_menu_sidebar(self):
        """Set up the sidebar for the Main Menu."""
        new_sidebar = self.main_menu_page.setup_sidebar()
        self.update_sidebar(new_sidebar)

    def setup_sr_counter_sidebar(self):
        """Set up the sidebar for SR Counter."""
        new_sidebar = self.sr_counter_page.setup_sidebar()
        self.update_sidebar(new_sidebar)

    def update_sidebar(self, new_sidebar):
        """Replace the existing sidebar with the new one."""
        self.main_layout.removeWidget(self.sidebar)
        self.sidebar.deleteLater()

        self.sidebar = new_sidebar
        self.main_layout.addWidget(self.sidebar, 0, 0, 1, 1)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Adjust path to point to correct location of style.qss
    qss_file = os.path.join(os.path.dirname(__file__), "resources", "QSS", "style.qss")

    # Load QSS stylesheet
    try:
        with open(qss_file, "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print(f"Error: The file {qss_file} was not found.")

    window = ReportGeneratorApp()
    window.show()
    sys.exit(app.exec_())
