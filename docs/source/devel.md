# Development

For development, [Hatch](https://hatch.pypa.io/latest/why/) is used to manage
the virtual environment and dependencies.

## Repository

Clone the official ScySeqTools repository:

```bash
git clone git@github.com:scyseq-tools/scyseqtools.git
cd scyseqtools
```

If you prefer HTTPS:

```bash
git clone https://github.com/scyseq-tools/scyseqtools.git
cd scyseqtools
```

## Hatch Setup

Make sure Hatch is installed in your default Python environment:

```bash
hatch --version
```

If it is not installed, you can install it using pip:

```bash
python -m pip install hatch
```

## Development Installation / Activation

Activate the project environment from the repository root:

```bash
hatch shell
```

Install ScySeqTools in editable mode:

```bash
python -m pip install -e .
```

To deactivate the environment, run:

```bash
exit
```

## Virtual Environment Setup

Hatch manages virtual environments for this project. Virtual environments can be
stored in a centralized location by adding the following to
`~/.config/hatch/config.toml`:

```toml
[envs]
storage.path = "~/_virtualenvs/hatch_envs"
```

This configuration centralizes all environments in one directory for easier
management across projects.

## Building Documentation

To generate HTML documentation from the repository root, run:

```bash
hatch run docs:build
```

The generated HTML documentation will be available in `docs/build/html/`. Open
`docs/build/html/index.html` in your browser to view the documentation.

You can also build the documentation manually by first activating the Hatch
environment:

```bash
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

## Diagrams

The documentation can include diagrams with the `mermaid` directive.

For the HTML documentation, Mermaid is rendered in the browser by
`sphinxcontrib-mermaid`. In `conf.py`, `mermaid_output_format` is set to `raw`
so the Sphinx build does not need Node, Chromium, `mmdc`, or the Mermaid CLI.
This is the format used by the GitHub Pages workflow.

Existing `.mmd` files can be included directly:

```rst
.. mermaid::
   _static/fig1.mmd
```

Browser-rendered Mermaid is meant for HTML output. If PDF or static image
outputs are needed later, add a separate Mermaid CLI rendering path and switch
that build to `png` or `svg` output.
