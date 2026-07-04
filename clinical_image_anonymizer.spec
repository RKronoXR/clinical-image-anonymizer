# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

project_root = Path.cwd()

datas = collect_data_files("gradio", include_py_files=True)
datas += collect_data_files("gradio_client")
datas += collect_data_files("safehttpx")
datas += collect_data_files("groovy")
datas.append(("src/webapp/styles.css", "src/webapp"))

a = Analysis(
    ["src/webapp/app.py"],
    pathex=[str(project_root)],
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
    [],
    exclude_binaries=True,
    name="Clinical Image Anonymizer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/icons/clinical_image_anonymizer.ico",
    version="version_info.txt",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Clinical Image Anonymizer",
)
