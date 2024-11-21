import os
import shutil
import subprocess


class AppBuilder:
    def __init__(self):
        self.spec_file = "app.spec"  # Update this if the spec file has a different name

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
            for file in os.listdir("."):
                if file.endswith(".spec"):
                    os.remove(file)
                    print(f"Removed spec file: {file}")
            print("Old builds cleaned successfully.")
        except Exception as e:
            print(f"Error cleaning old builds: {e}")

    def build_application(self):
        """Build the application using PyInstaller."""
        print("Building the application with PyInstaller...")
        try:
            # Ensure the spec file exists
            if not os.path.exists(self.spec_file):
                raise FileNotFoundError(f"Spec file '{self.spec_file}' not found. Please generate it or ensure it is in the correct location.")

            result = subprocess.run(
                ["pyinstaller", "--onefile", "--noconfirm", self.spec_file],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("Build complete. The executable is in the 'dist' directory.")
            else:
                print(f"Build failed: {result.stderr.strip()}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
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

    # Build the application
    builder.build_application()


if __name__ == "__main__":
    main()
