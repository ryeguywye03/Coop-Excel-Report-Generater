import os
import shutil
import subprocess
from modules.utils.file_helpers import FileHelper  # Import FileHelper to use get_spec_file_path


class AppBuilder:
    def __init__(self):
        self.spec_file = FileHelper.get_spec_file_path()  # Dynamically get the spec file path
        self.include_files = ["README.md", "version.txt", "requirements.txt", "logs"]  # Files and folders to include in the build

    def clean_old_builds(self):
        """Remove old build files and directories."""
        print("Cleaning old builds...")
        try:
            if os.path.exists("build"):
                shutil.rmtree("build")
                print("Removed 'build' directory.")
            if os.path.exists("dist"):
                shutil.rmtree("dist")
                print("Removed 'dist' directory.")
            # Do not overwrite the spec file if it exists
            if os.path.exists(self.spec_file):
                print(f"Spec file '{self.spec_file}' already exists. Not overwriting.")
            print("Old builds cleaned successfully.")
        except Exception as e:
            print(f"Error cleaning old builds: {e}")

    def ensure_files_exist(self):
        """Ensure that all critical files for packaging are present."""
        print("Checking for required files...")
        missing_files = [file for file in self.include_files if not os.path.exists(file)]
        if missing_files:
            print(f"Error: Missing required files: {', '.join(missing_files)}")
            raise FileNotFoundError(f"Missing required files: {', '.join(missing_files)}")
        print("All required files are present.")

    def prepare_logs_folder(self):
        """Ensure the logs folder exists and is writable."""
        logs_folder = "logs"
        if not os.path.exists(logs_folder):
            os.makedirs(logs_folder)
            print(f"Created 'logs' folder.")
        # Ensure the folder is writable
        test_log_file = os.path.join(logs_folder, "test_write.log")
        try:
            with open(test_log_file, "w") as test_file:
                test_file.write("Log folder is writable.\n")
            os.remove(test_log_file)  # Clean up test log
            print("'logs' folder is writable.")
        except IOError as e:
            print(f"Error: 'logs' folder is not writable. {e}")
            raise IOError(f"'logs' folder is not writable. {e}")

    def build_application(self):
        """Build the application using PyInstaller."""
        print("Building the application with PyInstaller...")
        print(f"Using spec file path: {self.spec_file}")
        try:
            # Ensure the spec file exists
            if not os.path.exists(self.spec_file):
                print(f"Spec file '{self.spec_file}' not found. Exiting build process.")
                raise FileNotFoundError(f"Spec file '{self.spec_file}' is missing.")

            # Build the application
            result = subprocess.run(
                ["pyinstaller", "--clean", "--noconfirm", self.spec_file],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("Build complete. The executable is in the 'dist' directory.")
            else:
                print(f"Build failed: {result.stderr.strip()}")
        except Exception as e:
            print(f"Unexpected error during build: {e}")

    def is_pyinstaller_installed(self):
        """Check if PyInstaller is installed."""
        try:
            result = subprocess.run(
                ["pyinstaller", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"PyInstaller version: {result.stdout.strip()}")
            return True
        except FileNotFoundError:
            print("PyInstaller is not installed. Please install it using 'pip install pyinstaller'.")
            return False
        except Exception as e:
            print(f"Unexpected error checking PyInstaller: {e}")
            return False


def main():
    builder = AppBuilder()

    # Check if PyInstaller is installed
    if not builder.is_pyinstaller_installed():
        return

    # Clean old builds
    builder.clean_old_builds()

    # Ensure required files are present
    try:
        builder.ensure_files_exist()
    except FileNotFoundError as e:
        print(f"Cannot proceed with the build: {e}")
        return

    # Prepare the logs folder
    try:
        builder.prepare_logs_folder()
    except IOError as e:
        print(f"Cannot proceed with the build: {e}")
        return

    # Build the application
    builder.build_application()


if __name__ == "__main__":
    main()
