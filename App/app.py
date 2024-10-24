import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from ui.main_menu import MainMenuUI  # Import Main Menu UI
from sr_counter import SRCounterUI  # Import the SR Counter UI from the sr_counter package
from utils import resource_path, LoggerManager  # Ensure utils has resource_path and LoggerManager
import os
import sys

class ReportGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Apply platform-specific stylesheet
        self.apply_stylesheet()

        self.logger = LoggerManager()  # Initialize logger
        self.logger.log_info("App initialized")

        # Get version number and set window title
        self.set_app_version()

        try:
            self.setup_ui()
            self.logger.log_info("UI setup completed")
        except Exception as e:
            self.logger.log_error(f"Error during UI setup: {e}")

    def apply_stylesheet(self):
        """Applies the correct QSS file based on the platform."""
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

    def set_app_version(self):
        """Sets the app version number from a version.txt file."""
        try:
            version = self.get_version()
            self.setWindowTitle(f"Excel Report Generator - v{version}")
        except FileNotFoundError:
            self.setWindowTitle("Excel Report Generator - Version not found")
            self.logger.log_error("version.txt not found")

    def setup_ui(self):
        """Setup the main UI layout using QStackedWidget to switch between pages."""
        self.central_widget = QStackedWidget()  # QStackedWidget to switch between full page setups
        self.setCentralWidget(self.central_widget)

        # Apply window size from settings (if available)
        window_size = self.get_window_size_from_settings()
        self.setMinimumSize(window_size["width"], window_size["height"])

        # Initialize the Main Menu and SR Counter pages
        self.main_menu = MainMenuUI(self)
        self.sr_counter = SRCounterUI(self)

        # Add both pages to the central widget stack
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.sr_counter)

        # Set default page to the Main Menu
        self.switch_to_main_menu()

    def get_window_size_from_settings(self):
        """Read the window size from a settings file."""
        # For demonstration purposes, let's assume a JSON settings file
        import json
        default_size = {"width": 1000, "height": 600}  # Fallback size
        settings_file = os.path.join(os.path.dirname(__file__), '../settings.json')
        
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
                return settings.get("window_size", default_size)
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.log_error(f"Error reading settings from {settings_file}")
            return default_size


    def switch_to_main_menu(self):
        """Switch to the Main Menu page."""
        self.central_widget.setCurrentWidget(self.main_menu)

    def switch_to_sr_counter(self):
        """Switch to the SR Counter page."""
        self.central_widget.setCurrentWidget(self.sr_counter)

    def get_version(self):
        """Reads the version number from the version.txt file."""
        version_path = os.path.join(os.path.dirname(__file__), '../version.txt')
        try:
            with open(version_path) as version_file:
                version = version_file.read().strip()
            return version
        except FileNotFoundError:
            self.logger.log_error(f"Error: version.txt not found at {version_path}")
        return "Version not found"


if __name__ == "__main__":
    # Initialize the PyQt5 application
    app = QApplication(sys.argv)

    # Disable logging for production
    logger_manager = LoggerManager(enable_logging=False)

    # Create and show the main window
    window = ReportGeneratorApp()
    window.show()

    sys.exit(app.exec_())
