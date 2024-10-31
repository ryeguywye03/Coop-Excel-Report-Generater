import platform
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from main_menu.main_menu import MainMenuUI  # Import Main Menu UI
from sr_counter import SRCounterUI  # Import the SR Counter UI from the sr_counter package
from utils import LoggerManager, AppSettings, FileHelper  # Ensure FileHelper is imported
import os
import sys
import json

class ReportGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize logger and log app start
        self.logger = LoggerManager(enable_logging=True)
        self.logger.log_info("App initialized")

        # Initialize app settings
        self.settings = AppSettings()  # Initialize settings here

        # Apply platform-specific stylesheet
        self.apply_stylesheet()

        # Get version number and set window title
        self.set_app_version()

        try:
            self.setup_ui()
            self.logger.log_info("UI setup completed")
        except Exception as e:
            self.logger.log_error(f"Error during UI setup: {e}")

    def apply_stylesheet(self):
        """Applies the stylesheet based on the current theme and platform."""
        # Reload settings to get the latest theme
        self.settings.reload_settings()
        
        theme = self.settings.get("theme", "dark").lower()
        platform_name = platform.system().lower()

        # Get the QSS file path using the helper method
        qss_file = FileHelper.get_qss_file_path(theme, platform_name)

        if qss_file is None:
            self.logger.log_error(f"Error: No QSS file found for theme '{theme}' on platform '{platform_name}'.")
            return  # Exit if no file found

        try:
            with open(qss_file, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            self.logger.log_error(f"Error: The file {qss_file} was not found.")

    def reload_stylesheet(self):
        """Reloads the stylesheet to reflect any theme changes."""
        self.apply_stylesheet()

    def set_app_version(self):
        """Sets the app version number from a version.txt file."""
        version_path = FileHelper.get_version_file_path('version.txt')
        try:
            with open(version_path) as version_file:
                version = version_file.read().strip()
                self.setWindowTitle(f"Excel Report Generator - v{version}")
                self.logger.log_info(f"App version set to v{version}")
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
        self.logger.log_info(f"Window size set to {window_size['width']}x{window_size['height']}")

        # Initialize the Main Menu and SR Counter pages
        self.main_menu = MainMenuUI(self)
        self.sr_counter = SRCounterUI(self)

        # Add both pages to the central widget stack
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.sr_counter)

        # Set default page to the Main Menu
        self.switch_to_main_menu()

    def get_window_size_from_settings(self):
        """Fetches the window size from settings or returns default."""
        default_size = {"width": 1000, "height": 600}  # Fallback size
        try:
            settings_file = FileHelper.get_settings_file_path()  # Use FileHelper to get settings path
            with open(settings_file, "r") as f:
                settings = json.load(f)
                self.logger.log_info("Settings loaded successfully")
                return settings.get("window_size", default_size)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.log_error(f"Error reading settings from {settings_file}: {e}")
            return default_size

    def switch_to_main_menu(self):
        """Switch to the Main Menu page."""
        self.central_widget.setCurrentWidget(self.main_menu)
        self.logger.log_info("Switched to Main Menu")

    def switch_to_sr_counter(self):
        """Switch to the SR Counter page."""
        self.central_widget.setCurrentWidget(self.sr_counter)
        self.logger.log_info("Switched to SR Counter")

    def get_version(self):
        """Reads the version number from the version.txt file."""
        version_path = FileHelper.get_resource_file_path('version.txt')  # Use FileHelper to get version path
        try:
            with open(version_path) as version_file:
                version = version_file.read().strip()
                self.logger.log_info(f"Version read from {version_path}: {version}")
            return version
        except FileNotFoundError:
            self.logger.log_error(f"Error: version.txt not found at {version_path}")
        return "Version not found"


if __name__ == "__main__":
    # Initialize the PyQt6 application
    app = QApplication(sys.argv)

    # Create and show the main window
    window = ReportGeneratorApp()
    window.show()

    sys.exit(app.exec())
