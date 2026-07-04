# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import importlib.util

from PyInstaller.utils.hooks import collect_data_files, collect_submodules


project_root = Path.cwd()


def package_file(package_name: str, relative_file: str, destination: str) -> tuple[str, str]:
    """Return a PyInstaller data tuple for one package data file."""
    spec = importlib.util.find_spec(package_name)
    if spec is None or spec.origin is None:
        raise RuntimeError(f"Could not locate package: {package_name}")

    package_dir = Path(spec.origin).parent
    source = package_dir / relative_file

    if not source.exists():
        raise RuntimeError(f"Required package file not found: {source}")

    return (str(source), destination)


datas = []
datas += collect_data_files("gradio", include_py_files=True)
datas += collect_data_files("gradio_client", include_py_files=True)
datas += collect_data_files("safehttpx")
datas += collect_data_files("groovy")

# Explicitly required by gradio_client.serializing at runtime.
datas.append(package_file("gradio_client", "types.json", "gradio_client"))

# Project assets.
datas.append(("src/webapp/styles.css", "src/webapp"))
datas.append(("assets/icons/clinical_image_anonymizer.ico", "assets/icons"))
datas.append(("version_info.txt", "."))

hiddenimports = []
hiddenimports += collect_submodules("gradio")
hiddenimports += collect_submodules("gradio_client")
hiddenimports += collect_submodules("safehttpx")
hiddenimports += collect_submodules("groovy")


a = Analysis(
    ["src/webapp/app.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
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