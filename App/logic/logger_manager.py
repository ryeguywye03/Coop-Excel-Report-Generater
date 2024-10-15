import logging
import os
from datetime import datetime

class LoggerManager:
    def __init__(self, log_dir="logs"):
        """Initializes the logger, setting up file and console handlers."""
        self.log_dir = log_dir
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)
        self.setup_logging()

    def setup_logging(self):
        """Sets up file and console handlers for logging."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Create log file based on the current date
        log_file = os.path.join(self.log_dir, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")

        # File handler for logging to a file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        # Stream handler for console output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)
