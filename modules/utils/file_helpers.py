import sys
import os
import pandas as pd
from datetime import datetime


class FileHelper:
    PRINT_ENABLED = False  # Set this to True to enable print statements

    @staticmethod
    def environment_check(print_env=False):
        """Check if the application is running in a bundled state or not."""
        env = 'bundle' if getattr(sys, 'frozen', False) else 'development'
        if FileHelper.PRINT_ENABLED and print_env:
            print(f"Current environment: {env}")
        return env

    @staticmethod
    def resource_path(relative_path):
        """
        Get the absolute path to a resource.
        Works in both development and PyInstaller bundle modes.
        """
        try:
            if getattr(sys, 'frozen', False):  # Check if running in a PyInstaller bundle
                base_path = sys._MEIPASS  # Path to the temporary folder for bundled resources
            else:  # Running in development mode
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

            # Combine the base path with the relative path
            final_path = os.path.normpath(os.path.join(base_path, relative_path))

            if FileHelper.PRINT_ENABLED:
                print(f"[FileHelper] Resolved resource path: {final_path}")

            return final_path
        except Exception as e:
            print(f"[FileHelper] Error resolving resource path for {relative_path}: {e}")
            raise

    @staticmethod
    def get_settings_file_path():
        """Get the path to the settings.json file."""
        return FileHelper.resource_path(os.path.join('resources', 'config', 'settings.json'))

    @staticmethod
    def get_excel_file_path(filename):
        """Get the path to an Excel file in the resources/Excel folder."""
        return FileHelper.resource_path(os.path.join('resources', 'Excel', filename))

    @staticmethod
    def get_json_file_path(filename):
        """Get the path to a JSON file in the resources/data folder."""
        return FileHelper.resource_path(os.path.join('resources', 'data', filename))

    @staticmethod
    def get_version_file_path():
        """Get the path to the version.txt file."""
        return FileHelper.resource_path('version.txt')

    @staticmethod
    def get_spec_file_path():
        """Get the path to the app.spec file."""
        return FileHelper.resource_path('app.spec')

    @staticmethod
    def get_qss_file_path(theme, platform):
        """Get the path to the QSS file based on the theme and platform."""
        if platform.lower() == "darwin":  # macOS
            path = FileHelper.resource_path(os.path.join('resources', 'styles', 'mac', f'mac_{theme}_style.qss'))
        elif platform.lower() == "windows":  # Windows
            path = FileHelper.resource_path(os.path.join('resources', 'styles', 'windows', f'windows_{theme}_style.qss'))
        else:
            path = None  # Handle other platforms as needed
        if FileHelper.PRINT_ENABLED:
            print(f"QSS file path for theme '{theme}' on platform '{platform}': {path}")
        return path

    @staticmethod
    def get_resource_file_path(relative_path):
        """Get resource paths relative to the app folder."""
        path = FileHelper.resource_path(os.path.join('resources', relative_path))
        if FileHelper.PRINT_ENABLED:
            print(f"Resource file path: {path}")
        return path

    @staticmethod
    def file_modified_after(file_path, reference_path):
        """Check if a file was modified after a reference file."""
        if not os.path.exists(file_path) or not os.path.exists(reference_path):
            return False
        file_mod_time = os.path.getmtime(file_path)
        ref_mod_time = os.path.getmtime(reference_path)
        if FileHelper.PRINT_ENABLED:
            print(f"{file_path} modified time: {datetime.fromtimestamp(file_mod_time)}")
            print(f"{reference_path} modified time: {datetime.fromtimestamp(ref_mod_time)}")
        return file_mod_time > ref_mod_time

    @staticmethod
    def read_excel(file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            if file_path.endswith('.xls'):
                df = pd.read_excel(file_path, engine='xlrd')
            else:
                df = pd.read_excel(file_path, engine='openpyxl')

            if df.empty:
                raise ValueError("Excel file is empty.")
            return df
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None

    @staticmethod
    def read_file(file_path):
        """General method to read either CSV or Excel files based on the extension."""
        if file_path.endswith(('.csv', '.txt')):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return FileHelper.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    @staticmethod
    def json_file_exists(json_path):
        """Check if a JSON file exists."""
        exists = os.path.exists(json_path)
        if FileHelper.PRINT_ENABLED:
            print(f"JSON file exists at {json_path}: {exists}")
        return exists
