# Updated app.spec for Excel Report Generator project
from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['App/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('App/assets/Excel', 'app/assets/Excel'),  # Include Excel assets
        ('App/assets/json', 'app/assets/json'),  # Include JSON assets
        ('App/assets/QSS/mac', 'app/assets/QSS/mac'),  # Mac QSS files
        ('App/assets/QSS/windows', 'app/assets/QSS/windows'),  # Windows QSS files
        ('App/dialogs', 'app/dialogs'),  # Place dialogs in the app folder
        ('App/main_menu', 'app/main_menu'),  # Place main_menu in the app folder
        ('App/sr_counter', 'app/sr_counter'),  # Place sr_counter in the app folder
        ('App/utils', 'app/utils'),  # Place utils in the app folder
        ('logs', 'app/logs'),  # Log files
        ('config', 'app/config'),  # Place config in the app folder
        ('version.txt', 'app/'),  # Place version.txt in root
        ('requirements.txt', 'app/'),  # Place requirements.txt in root
        ('README.md', 'app/'),  # Place README.md in root
        ('setup.py', 'app/'),  # Place setup.py in root
    ],
    hiddenimports=collect_submodules('App'),  # Collect all submodules under App
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
