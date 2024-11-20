from PyInstaller.utils.hooks import collect_data_files
import os

def get_app_data_paths():
    app_data_paths = []

    # Collect resources from `resources`
    app_data_paths.extend(collect_data_files(os.path.join('resources', 'Excel')))
    app_data_paths.extend(collect_data_files(os.path.join('resources', 'data')))
    app_data_paths.extend(collect_data_files(os.path.join('resources', 'config')))
    app_data_paths.extend(collect_data_files(os.path.join('resources', 'styles', 'mac')))
    app_data_paths.extend(collect_data_files(os.path.join('resources', 'styles', 'windows')))

    # Add logs directory (empty directory won't be included, ensure logs exist)
    app_data_paths.append(('logs', 'logs'))

    # Include version and requirements files
    app_data_paths.append(('version.txt', ''))
    app_data_paths.append(('requirements.txt', ''))
    app_data_paths.append(('README.md',''))

    return app_data_paths

# Analysis
a = Analysis(
    ['app.py'],  # Main entry script
    pathex=[],  # Path to modules if outside the current directory
    binaries=[],  # Include binaries if any
    datas=get_app_data_paths(),  # Dynamically add resources
    hiddenimports=[],  # Add any hidden imports
    hookspath=[],  # Custom hooks if any
    runtime_hooks=[],
    excludes=[],  # Exclude unnecessary modules or packages
    noarchive=False,  # Bundle all files into a single executable
    optimize=2,  # Optimize bytecode
)

# Build the executable
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ExcelReportGenerator',  # Name of the executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for a console application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Collect resources and binaries
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ExcelReportGenerator',
)
