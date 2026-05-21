# codix-suite

Codix is a Python toolkit for coding and analysing behaviours. It currently
provides two command line launchers:

- `codix-encoder`
- `codix-analyser`

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
cd path/to/codix-suite
```

Replace `path/to/codix-suite` with the folder where you cloned or downloaded
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
(codix) ...
```

That means you are inside the Codix virtual environment.

### 4. Install Codix in Editable Mode

Inside the Hatch shell, install the current project:

```sh
python -m pip install -e .
```

The `-e` option means "editable": Python imports Codix directly from this source
folder, so local code changes are picked up without reinstalling every time.

### 5. Verify the Install

```sh
python -m pip show codix
python -c "import codix; print(codix.__file__)"
python -c "import codix.encoder.main; print('ok')"
```

If the last command prints `ok`, the package import works.

## Run Codix

Inside the Hatch shell:

```sh
codix-encoder
```

or:

```sh
codix-analyser
```

The encoder opens a graphical interface and asks you to choose a working
directory. Codix expects or creates `media` and `data` folders inside that
working directory.

### Encoder Window Layout

By default, the encoder opens with the classic single-window layout. To split
the encoder into separate Information, Control, and Coding framework windows,
add this to the `config.ini` file in your Codix working directory:

```ini
[application]
encoder_layout = detached
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


# Tools used in this package:

[![Sphinx](https://img.shields.io/badge/docs-Sphinx-blue)](https://www.sphinx-doc.org/)
[![pytest](https://img.shields.io/badge/tests-pytest-blue)](https://docs.pytest.org/)
[![Hatch](https://img.shields.io/badge/project-Hatch-blue)](https://hatch.pypa.io/latest/)
[![doctest](https://img.shields.io/badge/tests-doctest-blue)](https://docs.python.org/3/library/doctest.html)
