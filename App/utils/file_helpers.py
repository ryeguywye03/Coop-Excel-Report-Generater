import sys
import os

class FileHelper:
    PRINT_ENABLED = False  # Set this to True to enable print statements

    @staticmethod
    def environment_check(print_env=False):
        """Check if the application is running in a bundled state or not.
   
        Args:
            print_env (bool): If True, print the current environment.
   
        Returns:
            str: 'bundle' if running in a bundled state, otherwise 'development'.
        """
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
            internal_path = os.path.join(base_path, '_internal', 'app')
            final_path = os.path.join(internal_path, relative_path)
            if FileHelper.PRINT_ENABLED:
                print(f"Using PyInstaller base path: {internal_path}")
        else:
            # If running in a script (development)
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            final_path = os.path.join(base_path, relative_path)
            if FileHelper.PRINT_ENABLED:
                print(f"Using development base path: {base_path}")
        
        if FileHelper.PRINT_ENABLED:
            print(f"Final resource path: {final_path}")
        return final_path

    @staticmethod
    def get_settings_file_path():
        """Get the path to the settings.json file."""
        return FileHelper.resource_path('config/settings.json')

    @staticmethod
    def get_excel_file_path(filename):
        """Get the path to an Excel file in the assets folder."""
        return FileHelper.resource_path(os.path.join('assets', 'Excel', filename))

    @staticmethod
    def get_json_file_path(filename):
        """Get the path to a JSON file in the assets/json folder."""
        return FileHelper.resource_path(os.path.join('assets', 'json', filename))

    @staticmethod
    def get_version_file_path():
        """Get the path to the version.txt file."""
        return FileHelper.resource_path(os.path.join('..', 'version.txt'))

    @staticmethod
    def get_qss_file_path(theme, platform):
        """Get the path to the QSS file based on the theme and platform."""
        if platform.lower() == "darwin":  # macOS
            path = FileHelper.resource_path(os.path.join('assets', 'QSS', 'mac', f'mac_{theme}_style.qss'))
        elif platform.lower() == "windows":  # Windows
            path = FileHelper.resource_path(os.path.join('assets', 'QSS', 'windows', f'windows_{theme}_style.qss'))
        else:
            path = None  # Handle other platforms as needed
        if FileHelper.PRINT_ENABLED:
            print(f"QSS file path for theme '{theme}' on platform '{platform}': {path}")
        return path

    @staticmethod
    def get_resource_file_path(relative_path):
        """Get resource paths relative to the app folder."""
        path = FileHelper.resource_path(os.path.join('assets', relative_path))
        if FileHelper.PRINT_ENABLED:
            print(f"Resource file path: {path}")
        return path
