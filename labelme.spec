# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('osam', include_py_files=False)
datas += [("labelme/config/default_config.yaml", "labelme/config")]

import os

def collect_labelme_images():
    image_data = []
    image_extensions = ('.png', '.svg', '.ico', '.icns')

    src_dir = os.path.join('labelme', 'icons')
    for root, _, files in os.walk(src_dir):
        for f in files:
            if f.lower().endswith(image_extensions):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, '.')  # maintain full relative path
                print("added: " + full_path + " rel path: " + root)
                image_data.append((full_path, 'labelme/icons'))
    return image_data

datas += collect_labelme_images()


a = Analysis(
    ['labelme\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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
    name='labelme',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
