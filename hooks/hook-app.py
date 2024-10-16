from PyInstaller.utils.hooks import collect_data_files

# Collect all assets (Excel files, JSON files, etc.)
datas = collect_data_files('assets')

# Optionally, include specific folders like QSS for styles
datas += collect_data_files('assets/QSS')
