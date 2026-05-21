"""Configuration loading for the encoder package."""

import configparser
import os
from importlib.resources import files


CONFIG_FILENAME = "config.ini"
VALID_ENCODER_LAYOUTS = ("embedded", "detached")


def load_encoder_config(cwd=None, required_sections=()):
    """Load encoder configuration.

    A config file in the Codix working directory overrides the bundled defaults.
    """
    config = configparser.ConfigParser()
    config.read_string(
        files("codix.encoder").joinpath(CONFIG_FILENAME).read_text(encoding="utf-8")
    )

    if cwd is not None:
        local_config = os.path.join(cwd, CONFIG_FILENAME)
        if os.path.exists(local_config):
            config.read(local_config)

    missing_sections = [
        section for section in required_sections if not config.has_section(section)
    ]
    if missing_sections:
        names = ", ".join(missing_sections)
        raise ValueError(f"Missing encoder config section: {names}")

    return config


def get_encoder_layout(cwd=None):
    """Return the configured encoder window layout."""
    config = load_encoder_config(cwd, required_sections=("application",))
    layout = config["application"].get("encoder_layout", "embedded").strip().lower()

    if layout not in VALID_ENCODER_LAYOUTS:
        valid_layouts = ", ".join(VALID_ENCODER_LAYOUTS)
        raise ValueError(
            f"Invalid encoder_layout: {layout!r}. "
            f"Use one of: {valid_layouts}."
        )

    return layout
