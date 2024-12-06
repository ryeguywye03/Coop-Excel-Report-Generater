import os
import requests
import subprocess
import ctypes
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from modules.utils.file_helpers import FileHelper
from modules.windows.main import MainWindow
from modules.utils.logger_manager import LoggerManager

class AppManager:
    def __init__(self, app, logger):
        self.app = app
        self.logger = logger
        self.current_version = None
        self.version_file = FileHelper.get_version_file_path()
        self.update_url = "https://raw.githubusercontent.com/ryeguywye03/Coop-Excel-Report-Generater/main/version.txt"

    def set_app_version(self, main_window):
        """Set the application version from version.txt."""
        try:
            with open(self.version_file, 'r') as version_file:
                self.current_version = version_file.read().strip()
                main_window.setWindowTitle(f"Excel Report Generator - v{self.current_version}")
                self.logger.log_info(f"App version set to v{self.current_version}")
                print(f"Current version: v{self.current_version}")
        except FileNotFoundError:
            main_window.setWindowTitle("Excel Report Generator - Version not found")
            self.logger.log_error("version.txt not found")
            print("Error: version.txt not found")
        except Exception as e:
            self.logger.log_error(f"Error reading version.txt: {e}")
            print(f"Error reading version.txt: {e}")

    def check_for_update(self):
        """Check for updates and log/print the results."""
        self.logger.log_info("Checking for updates...")
        print("Checking for updates...")
        try:
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                latest_version = response.text.strip()
                print(f"Fetched version from URL: v{latest_version}")
                self.logger.log_info(f"Fetched version from URL: v{latest_version}")

                if self.current_version is None:
                    self.logger.log_warning("Current version not set. Cannot determine if an update is available.")
                    print("Current version not set. Cannot determine if an update is available.")
                elif self.current_version < latest_version:
                    self.logger.log_warning(f"New version available: v{latest_version}. Current version: v{self.current_version}")
                    print(f"A new version {latest_version} is available. Updating...")
                    self.perform_update()
                else:
                    self.logger.log_info("You are using the latest version.")
                    print("You are using the latest version.")
            else:
                self.logger.log_error(f"Failed to fetch update information. Status code: {response.status_code}")
                print(f"Failed to fetch update information. Status code: {response.status_code}. Running the current version.")
        except requests.exceptions.RequestException as e:
            self.logger.log_error(f"Error checking for updates: {e}")
            print(f"Failed to check for updates due to a network issue. Proceeding with the current version.")
        except Exception as e:
            self.logger.log_error(f"Unexpected error checking for updates: {e}")
            print(f"Unexpected error checking for updates. Proceeding with the current version.")

    def perform_update(self):
        """Perform the update using Git pull."""
        self.logger.log_info("Attempting to update the application...")
        print("Attempting to update the application...")
        try:
            if not self.is_git_installed():
                self.logger.log_error("Git is not installed. Cannot perform update.")
                print("Git is not installed on this system. Please install Git to enable updates.")
                return

            result = subprocess.run(
                ["git", "pull"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                self.logger.log_info("Update successful. Please restart the application.")
                print("Update successful. Please restart the application.")
            else:
                self.logger.log_error(f"Update failed: {result.stderr.strip()}")
                print(f"Update failed: {result.stderr.strip()}")
        except Exception as e:
            self.logger.log_error(f"Error during update: {e}")
            print(f"Error during update: {e}")

    def is_git_installed(self):
        """Check if Git is installed."""
        try:
            subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    def check_network_drive(self):
        """Check if the application is running from a network drive and display a warning dialog."""
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            drive_type = ctypes.windll.kernel32.GetDriveTypeW(path[:3])

            if drive_type == 4:
                self.logger.log_warning("App is running from a network drive.")
                self.show_network_drive_warning()
                return True
            return False
        except Exception as e:
            self.logger.log_error(f"Error checking drive type: {e}")
            return False

    def show_network_drive_warning(self):
        """Show a warning dialog about running the app from a network drive."""
        message = (
            "It looks like the application is running from a network drive. "
            "To ensure proper functionality, please follow these steps:\n\n"
            "1. Close the application.\n"
            "2. Copy the entire 'dist' folder (including the .exe file) to your Desktop or another local drive.\n"
            "3. Run the application from the new location.\n\n"
            "If you need assistance, contact your IT department."
        )

        warning_dialog = QMessageBox()
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Network Drive Detected")
        warning_dialog.setText("Application is running from a network drive.")
        warning_dialog.setInformativeText(message)
        warning_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        warning_dialog.exec()

    def initialize_app(self, main_window):
        """Initialize the app."""
        if self.check_network_drive():
            return
        self.set_app_version(main_window)
        self.check_for_update()





def main():
    app = QApplication(sys.argv)

    # Initialize the logger
    logger = LoggerManager(enable_logging=True)
    logger.log_info("App initialized")

    # Initialize AppManager
    app_manager = AppManager(app, logger)

    # Create and show the main window
    window = MainWindow()
    app_manager.set_app_version(window)

    # Check for updates
    app_manager.check_for_update()

    # Show the main window
    window.show()

    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
