# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files


repo_root = Path(SPECPATH).parents[1]
src_dir = repo_root / "src"
pmw_datas = collect_data_files("Pmw", include_py_files=True)

hiddenimports = [
    "Pmw",
    "numpy",
    "scyseq",
    "scyseq.algorithmic",
    "scyseq.information",
    "scyseq.io",
    "scyseq.operations",
    "scyseq.sequence",
    "scyseq.stochastic",
    "tkinter",
    "tkinter.filedialog",
    "tkinter.messagebox",
]


a = Analysis(
    [str(src_dir / "scyseqtools" / "analyser" / "main.py")],
    pathex=[str(src_dir)],
    binaries=[],
    datas=pmw_datas,
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
    name="ScySeq Analyser",
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
    name="ScySeq Analyser",
)

app = BUNDLE(
    coll,
    name="ScySeq Analyser.app",
    icon=None,
    bundle_identifier="org.scyseqtools.analyser",
)
