import logging
import os
from datetime import datetime

class LoggerManager:
    _instance = None  # To enforce singleton pattern

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_dir="logs", enable_logging=True):
        """Initializes the logger, setting up file and console handlers."""
        if self._initialized:  # Prevent reinitialization
            return
        
        self.log_dir = log_dir
        self.logger = logging.getLogger("AppLogger")  # Use "AppLogger" as the name
        self.logger.setLevel(logging.DEBUG)
        self.enable_logging = enable_logging
        
        if self.enable_logging and not self.logger.hasHandlers():  # Prevent multiple handlers
            self.setup_logging()
        
        self._initialized = True

    def setup_logging(self):
        """Sets up file and console handlers for logging."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Create log file based on the current date
        log_file = os.path.join(self.log_dir, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")

        # File handler for logging to a file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - AppLogger - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        # Stream handler for console output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)

        # Add handlers to the logger only if they are not already added
        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def log_info(self, message):
        """Logs an informational message."""
        if self.enable_logging:
            self.logger.info(message)

    def log_debug(self, message):
        """Logs a debug message."""
        if self.enable_logging:
            self.logger.debug(message)

    def log_warning(self, message):
        """Logs a warning message."""
        if self.enable_logging:
            self.logger.warning(message)

    def log_error(self, message):
        """Logs an error message."""
        if self.enable_logging:
            self.logger.error(message)

    def log_critical(self, message):
        """Logs a critical message."""
        if self.enable_logging:
            self.logger.critical(message)
