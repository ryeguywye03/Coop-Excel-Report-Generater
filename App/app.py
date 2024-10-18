import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QGridLayout
from ui.main_menu import MainMenuUI
from ui.sr_counter_ui import SRCounterUI
from logic.logger_manager import LoggerManager
from utils import resource_path  # Import from utils for file paths
import os
import sys

# Define AppDelegate before it's used in macOS-specific logic
if platform.system() == "Darwin":  # macOS
    from Foundation import NSObject
    from AppKit import NSApp, NSApplication

    class AppDelegate(NSObject):
        def applicationSupportsSecureRestorableState_(self, app):
            return True


class ReportGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Use resource_path for file paths
        if platform.system() == "Darwin":  # macOS
            qss_file = resource_path(os.path.join('assets', 'QSS', 'mac_style.qss'))
        elif platform.system() == "Windows":  # Windows
            qss_file = resource_path(os.path.join('assets', 'QSS', 'windows_style.qss'))
        else:
            qss_file = resource_path(os.path.join('assets', 'QSS', 'default_style.qss'))

        try:
            with open(qss_file, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Error: The file {qss_file} was not found.")

        self.logger = LoggerManager()  # Initialize logger
        self.logger.log_info("App initialized")

        # Get version number and set window title
        try:
            version = self.get_version()
            self.setWindowTitle(f"Excel Report Generator - v{version}")
        except FileNotFoundError:
            self.setWindowTitle("Excel Report Generator - Version not found")
            self.logger.log_error("version.txt not found")

        try:
            self.setup_ui()
            self.logger.log_info("UI setup completed")
        except Exception as e:
            self.logger.log_error(f"Error during UI setup: {e}")

    def setup_ui(self):
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
        self.sidebar.hide()  # Hide before removing
        self.main_layout.removeWidget(self.sidebar)
        self.sidebar.deleteLater()
        
        self.sidebar = new_sidebar
        self.main_layout.addWidget(self.sidebar, 0, 0, 1, 1)
        self.sidebar.show()  # Show the new sidebar


    def get_version(self):
        """Reads the version number from the version.txt file."""
        version_path = os.path.join(os.path.dirname(__file__), '../version.txt')  # Use resource_path to find version.txt
        try:
            with open(version_path) as version_file:
                version = version_file.read().strip()
            return version
        except FileNotFoundError:
            self.logger.log_error(f"Error: version.txt not found at {version_path}")
        return "Version not found"


if __name__ == "__main__":
    # For macOS
    if platform.system() == "Darwin":
        # Initialize the macOS application
        app = NSApplication.sharedApplication()
        delegate = AppDelegate.alloc().init()

        if NSApp is not None:
            NSApp.setDelegate_(delegate)

    # Initialize the PyQt5 application
    app = QApplication(sys.argv)

    # Disable logging for production
    logger_manager = LoggerManager(enable_logging=False)

    # Create and show the main window
    window = ReportGeneratorApp()
    window.show()

    sys.exit(app.exec_())
