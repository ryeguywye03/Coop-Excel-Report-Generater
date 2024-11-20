import sys
import requests
import subprocess
from PyQt6.QtWidgets import QApplication
from modules.utils.logger_manager import LoggerManager
from modules.windows.main import MainWindow
from modules.utils.file_helpers import FileHelper


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
            response = requests.get(self.update_url)
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
                print(f"Failed to fetch update information. Status code: {response.status_code}")
        except Exception as e:
            self.logger.log_error(f"Error checking for updates: {e}")
            print(f"Error checking for updates: {e}")

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
