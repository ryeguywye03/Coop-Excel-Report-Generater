# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
import os

# Helper function to collect all app data paths
def get_app_data_paths():
    app_data_paths = []

    # Add resources folder in its entirety
    app_data_paths.append(('resources', 'resources'))

    # Add logs folder
    app_data_paths.append(('logs', 'logs'))

    # Include additional necessary files
    app_data_paths.append(('version.txt', '.'))
    app_data_paths.append(('requirements.txt', '.'))
    app_data_paths.append(('README.md', '.'))
    app_data_paths.append(('setup.py', '.'))

    return app_data_paths

# Analysis phase
a = Analysis(
    ['app.py'],                             # Main entry point for the application
    pathex=[],                              # Add custom paths if needed
    binaries=[],                            # Add any binary dependencies
    datas=get_app_data_paths(),             # Use the dynamic function to get data paths
    hiddenimports=collect_submodules('modules'),  # Collect all submodules under 'modules'
    hookspath=['hooks'],                    # Specify hook paths if any
    runtime_hooks=[],                       # Specify runtime hooks if any
    excludes=[],                            # Exclude specific modules if necessary
    noarchive=False,                        # Do not bundle the archive into a single file
    optimize=0,                             # Optimization level
)

# Python bytecode archive
pyz = PYZ(a.pure)

# Executable file
exe = EXE(
    pyz,
    a.scripts,                              # Main scripts from the analysis phase
    [],
    exclude_binaries=True,                  # Exclude binary dependencies
    name='app',                             # Name of the output executable
    debug=False,                            # Disable debug mode
    bootloader_ignore_signals=False,        # Bootloader signal handling
    strip=False,                            # Do not strip the executable
    upx=True,                               # Enable UPX compression
    console=False,                          # Disable the console window
    disable_windowed_traceback=False,       # Enable traceback for errors
    argv_emulation=False,                   # Disable argv emulation
    target_arch=None,                       # Use default architecture
    codesign_identity=None,                 # Specify code signing identity for macOS
    entitlements_file=None,                 # Entitlements for macOS
)

# Final collection phase
coll = COLLECT(
    exe,
    a.binaries,                             # Include all binaries
    a.datas,                                # Include all data files
    strip=False,                            # Do not strip binaries
    upx=True,                               # Enable UPX compression for collected files
    upx_exclude=[],                         # Exclude specific files from UPX compression
    name='app',                             # Name of the output directory
)
