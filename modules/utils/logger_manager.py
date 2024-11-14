import logging
import os
from logging.handlers import RotatingFileHandler
from PyQt6 import QtCore
from .file_helpers import FileHelper  # Correct relative import

class LoggerManager:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_dir="logs", enable_logging=True, console_level=logging.WARNING):
        """Initializes the logger, setting up file and console handlers."""
        if self._initialized:  # Prevent reinitialization
            return

        self.log_dir = FileHelper.resource_path(log_dir)
        self.logger = logging.getLogger("AppLogger")  # Use "AppLogger" as the name
        self.logger.setLevel(logging.DEBUG)  # Full debug level for file logging
        self.enable_logging = enable_logging
        self.console_level = console_level  # Set initial console logging level

        # Check if the log directory is writable
        if not self.check_log_directory():
            self.enable_logging = False  # Disable logging if log directory isn't writable

        # Set up logging handlers
        self.setup_logging()
        
        # Mark as initialized
        self._initialized = True

    def check_log_directory(self):
        """Check if the log directory is writable."""
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir)
            except OSError as e:
                self.logger.warning(f"Failed to create log directory {self.log_dir}: {e}")
                return False

        # Test write permission by attempting to create a temporary file
        test_file_path = os.path.join(self.log_dir, 'test.log')
        try:
            with open(test_file_path, 'w') as test_file:
                test_file.write("Test write permission.")
            os.remove(test_file_path)  # Clean up
            return True
        except Exception as e:
            self.logger.warning(f"Write permission check failed for {self.log_dir}: {e}")
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

        self.logger.log(level, message)

    def setup_logging(self):
        """Sets up separate file handlers for general and error logs, plus console output."""
        if not self.enable_logging:  # Skip if logging is disabled
            return

        # Install the Qt message handler
        QtCore.qInstallMessageHandler(self.qt_message_handler)

        # Configure file handlers for general and error logs
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

        # Configure the console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.console_level)  # Set initial level for console output
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)

        # Clear existing handlers to avoid duplicates
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Add the handlers to the logger
        self.logger.addHandler(general_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)

    def set_console_level(self, level):
        """Set the logging level for the console handler."""
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(level)
                self.console_level = level
                break

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
