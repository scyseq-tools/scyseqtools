# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs


repo_root = Path(SPECPATH).parents[1]
src_dir = repo_root / "src"

pymediainfo_datas = collect_data_files("pymediainfo")
pymediainfo_binaries = collect_dynamic_libs("pymediainfo")


a = Analysis(
    [str(src_dir / "scyseqtools" / "encoder" / "main.py")],
    pathex=[str(src_dir)],
    binaries=pymediainfo_binaries,
    datas=[
        (str(src_dir / "scyseqtools" / "encoder" / "config.ini"), "scyseqtools/encoder"),
        *pymediainfo_datas,
    ],
    hiddenimports=["platformdirs", "pymediainfo", "vlc"],
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
    name="scyseq-encoder",
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
)
