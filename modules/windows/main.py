import platform
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from modules.utils import LoggerManager, AppSettings, FileHelper
import os
import sys
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.logger = LoggerManager(enable_logging=True)
        self.logger.log_info("App initialized")

        self.settings = AppSettings()
        self.apply_stylesheet()
        self.set_app_version()

        self.setup_ui()

    def apply_stylesheet(self, force=False):
        current_theme = self.settings.get("theme", "dark").lower()
        platform_name = platform.system().lower()
        qss_file = FileHelper.get_qss_file_path(current_theme, platform_name)

        # Only apply stylesheet if the theme has changed or if forced
        if force or not hasattr(self, "_last_applied_theme") or self._last_applied_theme != current_theme:
            if qss_file:
                try:
                    with open(qss_file, "r") as file:
                        self.setStyleSheet(file.read())
                    self._last_applied_theme = current_theme
                    self.logger.log_info(f"Theme applied: {current_theme}")
                except FileNotFoundError:
                    self.logger.log_error(f"Stylesheet file not found: {qss_file}")
            else:
                self.logger.log_error(f"QSS file path not found for theme: {current_theme}")
        else:
            self.logger.log_debug("Theme not changed; it remains as {current_theme}")



    def set_app_version(self):
        version_path = FileHelper.get_version_file_path()
        
        # Log the directory from where the version file is expected to be found
        self.logger.log_info(f"Looking for version file at: {version_path}")

        try:
            with open(version_path) as version_file:
                version = version_file.read().strip()
                self.setWindowTitle(f"Excel Report Generator - v{version}")
                self.logger.log_info(f"App version set to v{version}")
        except FileNotFoundError:
            self.setWindowTitle("Excel Report Generator - Version not found")
            self.logger.log_error("version.txt not found")


    def setup_ui(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        window_size = self.get_window_size_from_settings()
        self.setMinimumSize(window_size["width"], window_size["height"])

        self.main_menu = None
        self.sr_counter = None
        self.switch_to_main_menu()

    def get_window_size_from_settings(self):
        default_size = {"width": 1000, "height": 600}
        try:
            settings_file = FileHelper.get_settings_file_path()
            with open(settings_file, "r") as f:
                settings = json.load(f)
                self.logger.log_info("Settings loaded successfully")
                return settings.get("window_size", default_size)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.log_error(f"Error reading settings from {settings_file}: {e}")
            return default_size

    def switch_to_main_menu(self):
        if self.main_menu is None:
            from modules.main_menu import MainMenuUI
            self.main_menu = MainMenuUI(self)
            self.central_widget.addWidget(self.main_menu)
        self.central_widget.setCurrentWidget(self.main_menu)
        self.logger.log_info("Switched to Main Menu")

    def switch_to_sr_counter(self):
        if self.sr_counter is None:
            from modules.sr_counter import SRCounterUI
            self.sr_counter = SRCounterUI(self)
            self.central_widget.addWidget(self.sr_counter)
        self.central_widget.setCurrentWidget(self.sr_counter)
        self.logger.log_info("Switched to SR Counter")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
