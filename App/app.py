import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from ui.main_menu import MainMenuUI
from ui.sr_counter_ui import SRCounterUI
from ui.settings_dialog import SettingsDialog

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget

from ui.main_menu import MainMenu
from ui.sr_counter_ui import SRCounterUI

class ReportGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Central widget and main layout setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Create a sidebar and main panel container
        self.sidebar_group = QWidget()  # To hold the sidebar
        self.main_panel = QStackedWidget()  # To switch between different main content panels

        # Add the sidebar and main panel to the layout
        self.main_layout.addWidget(self.sidebar_group, 0)  # Sidebar on the left
        self.main_layout.addWidget(self.main_panel, 1)     # Main panel on the right

        # Initialize the pages for Main Menu and SR Counter
        self.main_menu_page = MainMenu(self)
        self.sr_counter_page = SRCounterUI(self)

        # Add these pages to the stacked widget (main panel)
        self.main_panel.addWidget(self.main_menu_page)
        self.main_panel.addWidget(self.sr_counter_page)

        # Set the default page
        self.main_panel.setCurrentWidget(self.main_menu_page)

    def switch_to_sr_counter(self):
        """Switches to the SR Counter page."""
        self.main_panel.setCurrentWidget(self.sr_counter_page)

    def switch_to_main_menu(self):
        """Switches back to the Main Menu."""
        self.main_panel.setCurrentWidget(self.main_menu_page)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ReportGeneratorApp()
    window.show()
    sys.exit(app.exec_())
