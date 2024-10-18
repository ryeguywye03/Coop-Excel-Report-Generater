import sys
import os

def resource_path(relative_path):
    """ Get the absolute path to a resource. Works for dev and for PyInstaller """
    try:
        # If the app is packaged with PyInstaller, resources will be in the _MEIPASS directory
        base_path = sys._MEIPASS
        # This will point to the correct place when the app is packaged
        return os.path.join(base_path, 'App', relative_path)
    except AttributeError:
        # When running from the development environment
        # Adjust base path to be one level up
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        return os.path.join(base_path, 'App', relative_path)
