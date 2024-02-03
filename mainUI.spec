# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mainUI.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\Coding\\Python\\ControllerPs4\\Ps4MouseController\\myenv\\Lib\\site-packages\\eel\\eel.js', 'eel'), ('web', 'web'), ('userVariables.json', '.'), ('input_mapping.json', '.')],
    hiddenimports=['bottle_websocket'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='mainUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='mainUI',
)
