import sys
import os

def resource_path(relative_path):
    """ Get the absolute path to a resource. Works for dev and for PyInstaller. """
    try:
        base_path = sys._MEIPASS  # Path used when packaged
        print(f"Using PyInstaller MEIPASS base path: {base_path}")
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        print(f"Using development base path: {base_path}")

    final_path = os.path.join(base_path, relative_path)
    print(f"Final resource path: {final_path}")
    return final_path


def get_settings_file_path():
    """ Get the path to the settings.json file. """
    return resource_path('settings.json')


def get_excel_file_path(filename):
    """ Get the path to an Excel file in the assets folder. """
    return resource_path(os.path.join('assets', 'Excel', filename))


def get_json_file_path(filename):
    """ Get the path to a JSON file in the assets/json folder. """
    return resource_path(os.path.join('assets', 'json', filename))


def get_qss_file_path(theme, platform):
    """ Get the path to the QSS file based on the theme and platform. """
    if platform.lower() == "darwin":  # macOS
        return resource_path(os.path.join('assets', 'QSS', 'mac', f'mac_{theme}_style.qss'))
    elif platform.lower() == "windows":  # Windows
        return resource_path(os.path.join('assets', 'QSS', 'windows', f'windows_{theme}_style.qss'))
    else:
        return None  # Handle other platforms as needed


def get_resource_file_path(relative_path):
    """ Get resource paths relative to the app folder. """
    return resource_path(os.path.join('assets', relative_path))
