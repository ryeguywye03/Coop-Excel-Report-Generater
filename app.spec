from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import os

def get_app_data_paths():
    app_data_paths = []
    base_path = 'App'

    # Collecting relevant directories
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'assets', 'Excel')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'assets', 'json')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'assets', 'QSS', 'mac')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'assets', 'QSS', 'windows')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'dialogs')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'main_menu')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'sr_counter')))
    app_data_paths.extend(collect_data_files(os.path.join(base_path, 'utils')))
    app_data_paths.append((os.path.join(base_path, 'logs'), 'logs'))
    app_data_paths.append((os.path.join(base_path, 'config'), 'config'))
    
    # Include other necessary files
    app_data_paths.append(('version.txt', ''))
    app_data_paths.append(('requirements.txt', ''))
    app_data_paths.append(('README.md', ''))
    app_data_paths.append(('setup.py', ''))

    return app_data_paths

# In the Analysis call:
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
