# ScySeqTools

ScySeqTools is a Python toolkit for coding and analysing behaviours. It currently
provides two command line launchers:

- `scyseq-encoder`
- `scyseq-analyser`

## Requirements

- Python 3.9 or newer
- Hatch, used to create and manage the development virtual environment
- VLC 64-bit, required by the encoder through `python-vlc`
- `tkinter`
  - Windows: included with the standard Python installer
  - Ubuntu/Debian: `sudo apt install python3-tk`
  - macOS: install Python from python.org if `tkinter` is missing

On Windows, install 64-bit VLC from:

<https://www.videolan.org/vlc/download-windows.html>

After installing VLC, this file should exist:

```powershell
Test-Path "C:\Program Files\VideoLAN\VLC\libvlc.dll"
```

## Starter Setup

Clone or download the project, then open a terminal in the project folder.
On Windows, use PowerShell; on macOS or Linux, use your usual terminal.

```sh
cd path/to/scyseqtools
```

Replace `path/to/scyseqtools` with the folder where you cloned or downloaded
the project.

### 1. Check Python

```sh
python --version
```

You should see Python 3.9 or newer.

### 2. Check Whether Hatch Is Installed

```sh
hatch --version
```

If your terminal says `hatch` is not found or not recognized, install it:

```sh
python -m pip install hatch
```

Then check again:

```sh
hatch --version
```

### 3. Create and Enter the Hatch Environment

From the project root, run:

```sh
hatch shell
```

Your prompt should now start with something like:

```text
(scyseqtools) ...
```

That means you are inside the ScySeqTools virtual environment.

### 4. Install ScySeqTools in Editable Mode

Inside the Hatch shell, install the current project:

```sh
python -m pip install -e .
```

The `-e` option means "editable": Python imports ScySeqTools directly from this source
folder, so local code changes are picked up without reinstalling every time.

### 5. Verify the Install

```sh
python -m pip show scyseqtools
python -c "import scyseqtools; print(scyseqtools.__file__)"
python -c "import scyseqtools.encoder.main; print('ok')"
```

If the last command prints `ok`, the package import works.

## Run ScySeqTools

Inside the Hatch shell:

```sh
scyseq-encoder
```

or:

```sh
scyseq-analyser
```

The encoder opens a graphical interface and asks you to choose a working
directory. ScySeqTools expects or creates `media` and `data` folders inside that
working directory.

## User Configuration

On first run, ScySeqTools Encoder creates an editable config file in the
standard per-user config folder for your operating system:

```text
Windows: %APPDATA%\ScySeqTools\Encoder\config.ini
Ubuntu/Linux: ~/.config/ScySeqTools/Encoder/config.ini
macOS: ~/Library/Application Support/ScySeqTools/Encoder/config.ini
```

The app loads configuration in this order:

1. Bundled defaults inside the package or `.exe`.
2. The user-editable OS config file shown above.
3. A `config.ini` in the selected working directory, if present.

That means users can change global defaults in their user config folder, and a specific project
can override them by placing its own `config.ini` in the project working folder.
The last selected working directory is remembered in:

```text
Windows: %APPDATA%\ScySeqTools\Encoder\cwdfile.ini
Ubuntu/Linux: ~/.local/state/ScySeqTools/Encoder/cwdfile.ini
macOS: ~/Library/Application Support/ScySeqTools/Encoder/cwdfile.ini
```

### Encoder Window Layout

By default, the encoder opens with the classic single-window layout. To split
the encoder into separate Information, Control, and Coding framework windows,
add this to the AppData or project `config.ini` file:

```ini
[application]
encoder_layout = detached
```

## Download Applications

GitHub Actions builds downloadable encoder and analyser applications for
Windows, Ubuntu, macOS Intel, and macOS Apple Silicon. Each workflow run uploads
temporary build artifacts:

```text
ScySeqTools-Encoder-windows-x64-<tag>.zip
ScySeqTools-Encoder-ubuntu-22.04-x64-<tag>.tar.gz
ScySeqTools-Encoder-macos-x64-<tag>.zip
ScySeqTools-Encoder-macos-arm64-<tag>.zip
ScySeqTools-Analyser-windows-x64-<tag>.zip
ScySeqTools-Analyser-ubuntu-22.04-x64-<tag>.tar.gz
ScySeqTools-Analyser-macos-x64-<tag>.zip
ScySeqTools-Analyser-macos-arm64-<tag>.zip
SHA256SUMS.txt
```

The packaged encoder apps do not bundle VLC. Install VLC on the target machine
before running the encoder. On Windows, confirm this file exists:

```powershell
Test-Path "C:\Program Files\VideoLAN\VLC\libvlc.dll"
```

macOS builds are not Developer ID signed or notarized yet, so users may need to
right-click the app and choose **Open**, or allow it from macOS Privacy &
Security settings.

## Build Applications Locally

From the project root, install build dependencies:

```powershell
python -m pip install -e ".[dev,build]"
```

Then run the spec for your OS:

```powershell
# Windows
pyinstaller --clean --noconfirm packaging/pyinstaller/scyseq-encoder-windows.spec
pyinstaller --clean --noconfirm packaging/pyinstaller/scyseq-analyser-windows.spec
```

```sh
# Ubuntu/Linux
pyinstaller --clean --noconfirm packaging/pyinstaller/scyseq-encoder-linux.spec
pyinstaller --clean --noconfirm packaging/pyinstaller/scyseq-analyser-linux.spec
```

```sh
# macOS
pyinstaller --clean --noconfirm packaging/pyinstaller/scyseq-encoder-macos.spec
pyinstaller --clean --noconfirm packaging/pyinstaller/scyseq-analyser-macos.spec
```


## Run Tests

Inside the Hatch shell:

```sh
python -m pytest tests
```

## Build the Documentation

The documentation is built with Sphinx.

First enter the Hatch environment from the project root:

```sh
hatch shell
```

Then navigate to the docs folder and build the HTML files:

**On Windows:**
```bash
cd docs
./make.bat html
```

**On Linux/Mac:**
```bash
cd docs
make html
```

The generated HTML documentation will be available in `docs/build/html/`. Open `docs/build/html/index.html` in your browser to view the documentation.

## Contributing

Contributions to ScySeqTools are welcome!

To contribute:

1. Fork the official repository: [github.com/scyseq-tools/scyseqtools](https://github.com/scyseq-tools/scyseqtools).
2. Create a branch for your feature or bug fix.
3. Submit a pull request with a clear description of changes.
4. Ensure tests pass.


# Tools used in this package:

[![Sphinx](https://img.shields.io/badge/docs-Sphinx-blue)](https://www.sphinx-doc.org/)
[![pytest](https://img.shields.io/badge/tests-pytest-blue)](https://docs.pytest.org/)
[![Hatch](https://img.shields.io/badge/project-Hatch-blue)](https://hatch.pypa.io/latest/)
[![doctest](https://img.shields.io/badge/tests-doctest-blue)](https://docs.python.org/3/library/doctest.html)
