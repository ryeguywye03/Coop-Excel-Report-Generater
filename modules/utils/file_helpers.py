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
        """Get the absolute path to a resource. Works for dev and for PyInstaller."""
        if FileHelper.environment_check(print_env=False) == 'bundle':
            # If running in a bundle (PyInstaller)
            base_path = os.path.dirname(sys.executable)
            final_path = os.path.join(base_path, relative_path)
            if FileHelper.PRINT_ENABLED:
                print(f"Using PyInstaller base path: {base_path}")
        else:
            # If running in a script (development)
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Adjusted to locate resources directory
            final_path = os.path.join(base_path, relative_path)
            if FileHelper.PRINT_ENABLED:
                print(f"Using development base path: {base_path}")
        
        if FileHelper.PRINT_ENABLED:
            print(f"Final resource path: {final_path}")
        return final_path

    @staticmethod
    def get_settings_file_path():
        """Get the path to the settings.json file."""
        return FileHelper.resource_path(os.path.join('resources', 'config', 'settings.json'))

    @staticmethod
    def get_excel_file_path(filename):
        """Get the path to an Excel file in the resources/Excel folder."""
        return FileHelper.resource_path(os.path.join('resources', 'Excel', filename))
    
    @staticmethod
    def get_excel_type_path():
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
        """Read data from an Excel file and return it as a pandas DataFrame, handling both .xls and .xlsx formats."""
        if not os.path.exists(file_path):
            if FileHelper.PRINT_ENABLED:
                print(f"Excel file not found: {file_path}")
            return None
        try:
            # Use different engines based on file extension
            if file_path.endswith('.xls'):
                df = pd.read_excel(file_path, engine='xlrd')
            else:
                df = pd.read_excel(file_path, engine='openpyxl')
            
            if FileHelper.PRINT_ENABLED:
                print(f"Read data from {file_path}:\n{df}")
            return df  # Return DataFrame directly
        except Exception as e:
            if FileHelper.PRINT_ENABLED:
                print(f"Error reading Excel file {file_path}: {e}")
            return None


    @staticmethod
    def json_file_exists(json_path):
        """Check if a JSON file exists."""
        exists = os.path.exists(json_path)
        if FileHelper.PRINT_ENABLED:
            print(f"JSON file exists at {json_path}: {exists}")
        return exists
