import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import sys  # Import sys for environment check
from utils.file_helpers import FileHelper  # Ensure FileHelper is imported

class LoggerManager:
    _instance = None  # To enforce singleton pattern

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating new LoggerManager instance")
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance._initialized = False
        else:
            print("Using existing LoggerManager instance")
        return cls._instance

    def __init__(self, log_dir="logs", enable_logging=True):
        """Initializes the logger, setting up file and console handlers."""
        if self._initialized:  # Prevent reinitialization
            print("LoggerManager already initialized, skipping setup.")
            return

        print("Initializing LoggerManager...")
        self.log_dir = FileHelper.resource_path(log_dir)  # Use resource_path to find the log directory
        
        # Call environment check and print the current environment
        self.current_environment = FileHelper.environment_check(print_env=True)
        
        self.logger = logging.getLogger("AppLogger")  # Use "AppLogger" as the name
        self.logger.setLevel(logging.DEBUG)
        self.enable_logging = enable_logging

        # Check if log directory is writable before setting up logging
        if not self.check_log_directory():
            print("Log directory is not writable. Logging will be disabled.")
            self.enable_logging = False  # Disable logging if directory is not writable

        # Ensure setup_logging runs
        self.setup_logging()
        
        self._initialized = True
        print("Logger initialized:", self.enable_logging)
        print("Handlers added:", bool(self.logger.handlers))

    def check_log_directory(self):
        """Check if the log directory is writable."""
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir)
                print(f"Created log directory at {self.log_dir}")
            except OSError as e:
                print(f"Failed to create log directory {self.log_dir}: {e}")
                return False  # Return False if directory can't be created

        # Test write permission by attempting to create a temporary file
        test_file_path = os.path.join(self.log_dir, 'test.log')
        try:
            with open(test_file_path, 'w') as test_file:
                test_file.write("Test write permission.")
            os.remove(test_file_path)  # Remove the test file
            return True  # Write permission is granted
        except Exception as e:
            print(f"Write permission check failed for {self.log_dir}: {e}")
            return False  # Return False if write permission is denied

    def setup_logging(self):
        """Sets up separate file handlers for general and error logs, plus console output."""
        if not self.enable_logging:  # Skip if logging is disabled
            return

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # General log file handler with rotation
        general_log_file = os.path.join(self.log_dir, "app_general.log")
        general_handler = RotatingFileHandler(general_log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
        general_handler.setLevel(logging.INFO)
        general_format = logging.Formatter('%(asctime)s - AppLogger - %(levelname)s - %(message)s')
        general_handler.setFormatter(general_format)

        # Error log file handler with rotation
        error_log_file = os.path.join(self.log_dir, "app_errors.log")
        error_handler = RotatingFileHandler(error_log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        error_handler.setLevel(logging.ERROR)
        error_format = logging.Formatter('%(asctime)s - AppLogger - %(levelname)s - %(message)s')
        error_handler.setFormatter(error_format)

        # Console handler for real-time log output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)

        # Clear existing handlers to avoid duplicate logs if reinitializing
        self.logger.handlers.clear()

        # Add the handlers to the logger
        self.logger.addHandler(general_handler)
        self.logger.addHandler(error_handler)
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
