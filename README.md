# Excel Report Generator

An application designed to load and generate customized Excel reports from datasets with advanced filtering, sorting, and exclusion options.

## Features

- **Load Excel Files**: Easily import Excel files and view your data within the app.
- **Customizable Reports**: Select the columns you want in your report, and filter data by date ranges.
- **Exclusion Settings**: Exclude specific SR types or groups and optionally exclude rows with no location (0,0 coordinates).
- **Save as Excel**: Export your customized reports in Excel format.
- **Intuitive UI**: Simple and user-friendly interface built with PyQt5.

## Installation

To install and run the application, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ryeguywye03/Coop-Excel-Report-Generater.git
    cd excel-report-generator
    ```

2. **Set up a virtual environment** (optional, but recommended):
    - For Mac/Linux:
        ```bash
        python3 -m venv myenv
        source myenv/bin/activate
        ```
    - For Windows:
        ```bash
        python -m venv myenv
        myenv\Scripts\activate
        ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    python app.py
    ```

