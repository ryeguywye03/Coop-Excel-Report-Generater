import logging
import os
from logging.handlers import RotatingFileHandler
from PyQt6 import QtCore
from utils.file_helpers import FileHelper  # Ensure FileHelper is imported

class LoggerManager:
    _instance = None  # Singleton instance

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
            return

        print("Initializing LoggerManager...")
        self.log_dir = FileHelper.resource_path(log_dir)
        self.logger = logging.getLogger("AppLogger")  # Use "AppLogger" as the name
        self.logger.setLevel(logging.DEBUG)
        self.enable_logging = enable_logging

        # Check if the log directory is writable
        if not self.check_log_directory():
            print("Log directory is not writable. Disabling logging.")
            self.enable_logging = False

        # Set up logging handlers
        self.setup_logging()
        
        # Mark as initialized
        self._initialized = True
        print("LoggerManager initialized successfully")

    def check_log_directory(self):
        """Check if the log directory is writable."""
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir)
                print(f"Created log directory at {self.log_dir}")
            except OSError as e:
                print(f"Failed to create log directory {self.log_dir}: {e}")
                return False

        # Test write permission by attempting to create a temporary file
        test_file_path = os.path.join(self.log_dir, 'test.log')
        try:
            with open(test_file_path, 'w') as test_file:
                test_file.write("Test write permission.")
            os.remove(test_file_path)  # Clean up
            return True
        except Exception as e:
            print(f"Write permission check failed for {self.log_dir}: {e}")
            return False

    def qt_message_handler(self, mode, context, message):
        """Custom Qt message handler to direct Qt messages to Python's logging system."""
        if mode == QtCore.QtMsgType.QtDebugMsg:
            level = logging.DEBUG
        elif mode == QtCore.QtMsgType.QtInfoMsg:
            level = logging.INFO
        elif mode == QtCore.QtMsgType.QtWarningMsg:
            level = logging.WARNING
        elif mode == QtCore.QtMsgType.QtCriticalMsg:
            level = logging.CRITICAL
        else:
            level = logging.ERROR

        # Log the message using Python's logging module
        self.logger.log(level, message)

    def setup_logging(self):
        """Sets up separate file handlers for general and error logs, plus console output."""
        if not self.enable_logging:  # Skip if logging is disabled
            return

        # Install the Qt message handler
        QtCore.qInstallMessageHandler(self.qt_message_handler)

        # Configure Python's logging module with file and console handlers
        general_log_file = os.path.join(self.log_dir, "app_general.log")
        general_handler = RotatingFileHandler(general_log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
        general_handler.setLevel(logging.INFO)
        general_format = logging.Formatter('%(asctime)s - AppLogger - %(levelname)s - %(message)s')
        general_handler.setFormatter(general_format)

        error_log_file = os.path.join(self.log_dir, "app_errors.log")
        error_handler = RotatingFileHandler(error_log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        error_handler.setLevel(logging.ERROR)
        error_format = logging.Formatter('%(asctime)s - AppLogger - %(levelname)s - %(message)s')
        error_handler.setFormatter(error_format)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)

        # Clear existing handlers to avoid duplicates
        if self.logger.hasHandlers():
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
