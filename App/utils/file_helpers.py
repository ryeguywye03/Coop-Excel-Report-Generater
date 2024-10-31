import sys
import os

class FileHelper:
    @staticmethod
    def environment_check(print_env=True):
        """Check if the application is running in a bundled state or not.
   
        Args:
            print_env (bool): If True, print the current environment.
   
        Returns:
            str: 'bundle' if running in a bundled state, otherwise 'development'.
        """
        env = 'bundle' if getattr(sys, 'frozen', False) else 'development'
        if print_env:
            print(f"Current environment: {env}")
        return env

    @staticmethod
    def resource_path(relative_path):
        """Get the absolute path to a resource. Works for dev and for PyInstaller."""
        if FileHelper.environment_check() == 'bundle':
            # If running in a bundle (PyInstaller)
            # Set base path to the directory of the executable
            base_path = os.path.dirname(sys.executable)
            # Navigate to the _internal/app directory
            internal_path = os.path.join(base_path, '_internal', 'app')
            print(f"Using PyInstaller base path: {internal_path}")
            
            # Ensure the relative path is structured correctly within the internal directory
            final_path = os.path.join(internal_path, relative_path)
        else:
            # If running in a script (development)
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            print(f"Using development base path: {base_path}")
            
            # Ensure the relative path is structured correctly
            final_path = os.path.join(base_path, relative_path)

        print(f"Final resource path: {final_path}")
        return final_path


    @staticmethod
    def get_settings_file_path():
        """Get the path to the settings.json file."""
        return FileHelper.resource_path('config/settings.json')  # Adjust path as needed

    @staticmethod
    def get_excel_file_path(filename):
        """Get the path to an Excel file in the assets folder."""
        return FileHelper.resource_path(os.path.join('assets', 'Excel', filename))

    @staticmethod
    def get_json_file_path(filename):
        """Get the path to a JSON file in the assets/json folder."""
        return FileHelper.resource_path(os.path.join('assets', 'json', filename))

    @staticmethod
    def get_version_file_path(filename):
        """Get the path to the version.txt file."""
        return FileHelper.resource_path(os.path.join('..','version.txt'))

    @staticmethod
    def get_qss_file_path(theme, platform):
        """Get the path to the QSS file based on the theme and platform."""
        if platform.lower() == "darwin":  # macOS
            return FileHelper.resource_path(os.path.join('assets', 'QSS', 'mac', f'mac_{theme}_style.qss'))
        elif platform.lower() == "windows":  # Windows
            return FileHelper.resource_path(os.path.join('assets', 'QSS', 'windows', f'windows_{theme}_style.qss'))
        else:
            return None  # Handle other platforms as needed

    @staticmethod
    def get_resource_file_path(relative_path):
        """Get resource paths relative to the app folder."""
        return FileHelper.resource_path(os.path.join('assets', relative_path))
