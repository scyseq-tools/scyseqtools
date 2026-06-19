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
    [],
    exclude_binaries=True,
    name="ScySeq Encoder",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
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
    upx=False,
    upx_exclude=[],
    name="ScySeq Encoder",
)

app = BUNDLE(
    coll,
    name="ScySeq Encoder.app",
    icon=None,
    bundle_identifier="org.scyseqtools.encoder",
)
