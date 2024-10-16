from PyInstaller.utils.hooks import collect_data_files

# Collect all assets (Excel files, JSON files, etc.)
datas = collect_data_files('assets')

# Include QSS folder for styles
datas += collect_data_files('assets/QSS')

# Include assets folder for Excel files
datas += collect_data_files('assets/Excel')

# Include assets folder for JSON files
datas += collect_data_files('assets/JSON')

# Include config folder
datas += collect_data_files('config')

# Include logic folder if it has any required data files
datas += collect_data_files('logic')

# Include ui folder if it has any required data files
datas += collect_data_files('ui')

# Manually include extra files like version.txt, requirements.txt, README.md, and setup.py
datas += [('version.txt', '.'), ('requirements.txt', '.'), ('README.md', '.'), ('setup.py', '.')]

# Add the source code (App folder) so it's included in the package and accessible to users.
datas += collect_data_files('App')
