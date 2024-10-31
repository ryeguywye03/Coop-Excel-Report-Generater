from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import os

def get_app_data_paths():
    """Dynamically collect data file paths from the App directory."""
    app_data_paths = []
    base_path = os.path.join('App', 'assets')

    # Collect paths for assets
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'Excel')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'json')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'QSS/mac')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'QSS/windows')))
    app_data_paths.extend(collect_data_files('App/dialogs'))
    app_data_paths.extend(collect_data_files('App/main_menu'))
    app_data_paths.extend(collect_data_files('App/sr_counter'))
    app_data_paths.extend(collect_data_files('App/utils'))
    app_data_paths.append(('App/logs', 'app/logs'))
    app_data_paths.append(('App/config', 'app/config'))
    
    # Include other necessary files
    app_data_paths.append(('version.txt', 'app/'))
    app_data_paths.append(('requirements.txt', 'app/'))
    app_data_paths.append(('README.md', 'app/'))
    app_data_paths.append(('setup.py', 'app/'))

    return app_data_paths

a = Analysis(
    ['App/app.py'],
    pathex=[],
    binaries=[],
    datas=get_app_data_paths(),  # Use the dynamic function here
    hiddenimports=collect_submodules('App'),
    hookspath=['hooks'],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
