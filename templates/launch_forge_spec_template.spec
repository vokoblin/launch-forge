# -*- coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect all PyQt5 dependencies
binaries = []
datas = []
hiddenimports = []

# Collect PyQt5 and all its dependencies
for pkg in ['PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets']:
    b, d, h = collect_all(pkg)
    binaries.extend(b)
    datas.extend(d)
    hiddenimports.extend(h)

# Additional PyQt5 imports that may be missed
hiddenimports.extend(['PyQt5.sip', 'PyQt5.QtPrintSupport'])

a = Analysis(
    ['{main_file}'],
    pathex=[],
    binaries=binaries,
    datas=[{datas}] + datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='{output_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['{icon_path}'],
)