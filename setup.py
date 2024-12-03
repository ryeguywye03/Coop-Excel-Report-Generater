from setuptools import setup, find_packages
import os

def read_version():
    """Read the version from the version.txt file."""
    with open("version.txt", "r") as version_file:
        return version_file.read().strip()

setup(
    name='Excel_Report_Generator',
    version=read_version(),  # Get the version from version.txt
    description='An app to generate Excel reports',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/ryeguywye03/Coop-Excel-Report-Generater.git',
    python_requires='>=3.11.6',  # Specify the Python version here
    install_requires=[
        'et-xmlfile==1.1.0',
        'openpyxl==3.1.5',
        'pandas==2.2.3',
        'PyQt6',
        'PyQt6-Qt6',
        'PyQt6_sip',
        'python-dateutil==2.9.0.post0',
        'python-version==0.0.2',
        'pytz==2024.2',
        'six==1.16.0',
        'tzdata==2024.2',
        'XlsxWriter==3.2.0',
        'pyinstaller',
        'setuptools',  # Include setuptools
    ],
    entry_points={
        'console_scripts': [
            'excel-report-generator = app:main',
        ],
    },
)
