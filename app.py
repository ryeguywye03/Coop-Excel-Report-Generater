import sys
from PyQt6.QtWidgets import QApplication

from modules.utils.logger_manager import LoggerManager
from modules.windows.main import MainWindow

def main():
    app = QApplication(sys.argv)

    # Initialize the logger
    logger = LoggerManager(enable_logging=True)
    logger.log_info("App initialized")

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
