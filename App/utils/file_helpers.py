import sys
import os

def resource_path(relative_path):
    """ Get the absolute path to a resource. Works for dev and for PyInstaller """
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
    # Adjust this path to your preferred location of settings.json
    base_path = os.path.dirname(os.path.abspath(__file__))
    settings_path = os.path.join(base_path, '..', 'settings.json')  # Adjust this as needed
    return settings_path
