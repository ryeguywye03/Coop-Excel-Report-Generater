a = Analysis(
    ['App/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('App/assets', 'app/assets'),  # Place assets in the app folder
        ('App/config', 'app/config'),  # Place config in the app folder
        ('App/logic', 'app/logic'),    # Place logic in the app folder
        ('App/ui', 'app/ui'),          # Place ui in the app folder
        ('hooks', 'hooks'),  # Place hooks in root
        ('version.txt', '.'),  # Place version.txt in root
        ('requirements.txt', '.'),  # Place requirements.txt in root
        ('README.md', '.'),  # Place README.md in root
        ('setup.py', '.'),  # Place setup.py in root
    ],
    hiddenimports=[],
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

app = BUNDLE(
    coll,
    name='app.app',
    icon=None,
    bundle_identifier=None,
)
