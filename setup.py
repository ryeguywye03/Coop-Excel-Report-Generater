from setuptools import setup, find_packages

setup(
    name='Excel_Report_Generator',
    version='1.0.3',
    description='An app to generate Excel reports',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.11.6',  # Specify the Python version here
    install_requires=[
        'pandas',
        'numpy',
        'PyQt5',
        'openpyxl',
        'xlsxwriter',
        'et-xmlfile',
        'python-dateutil',
        'pytz',
        'tzdata',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'excel-report-generator = app:main',
        ],
    },
)
