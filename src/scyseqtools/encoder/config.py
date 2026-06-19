"""Configuration loading for the encoder package."""

import configparser
import os
from importlib.resources import files
from pathlib import Path

import platformdirs


APP_NAME = "ScySeqTools"
APP_COMPONENT_NAME = "Encoder"
CONFIG_FILENAME = "config.ini"
CWD_FILENAME = "cwdfile.ini"
VALID_ENCODER_LAYOUTS = ("embedded", "detached")


def bundled_config_text():
    """Return the default config distributed with the package."""
    return files("scyseqtools.encoder").joinpath(CONFIG_FILENAME).read_text(
        encoding="utf-8"
    )


def get_user_config_dir(config_dir=None):
    """Return the folder that stores user-editable encoder configuration."""
    if config_dir is not None:
        return Path(config_dir)

    return platformdirs.user_config_path(
        APP_NAME, appauthor=False, roaming=True
    ) / APP_COMPONENT_NAME


def get_user_config_path(config_dir=None):
    """Return the user-editable config.ini path."""
    return get_user_config_dir(config_dir) / CONFIG_FILENAME


def get_user_state_dir(config_dir=None):
    """Return the folder that stores user-specific encoder state."""
    if config_dir is not None:
        return Path(config_dir)

    return platformdirs.user_state_path(
        APP_NAME, appauthor=False, roaming=True
    ) / APP_COMPONENT_NAME


def ensure_user_config_file(config_dir=None):
    """Create the user-editable config.ini from defaults if it is missing."""
    config_path = get_user_config_path(config_dir)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if not config_path.exists():
        config_path.write_text(bundled_config_text(), encoding="utf-8")
    return config_path


def get_app_state_file_path(filename=CWD_FILENAME, config_dir=None):
    """Return an app-owned state file path inside the user state folder."""
    expanded = Path(os.path.expandvars(os.path.expanduser(filename)))
    if expanded.is_absolute():
        expanded.parent.mkdir(parents=True, exist_ok=True)
        return expanded

    state_path = get_user_state_dir(config_dir) / expanded
    state_path.parent.mkdir(parents=True, exist_ok=True)
    return state_path


def get_cwd_file_path(config=None, config_dir=None):
    """Return the file used to remember the last selected working directory."""
    if config is None:
        config = load_encoder_config(
            required_sections=("application",),
            config_dir=config_dir,
        )
    cwd_filename = config["application"].get("cwd_file", CWD_FILENAME)
    return get_app_state_file_path(cwd_filename, config_dir=config_dir)


def load_encoder_config(cwd=None, required_sections=(), config_dir=None):
    """Load encoder configuration.

    Defaults are loaded first, then the user-editable config, then an optional
    config file in the selected working directory.
    """
    config = configparser.ConfigParser()
    config.read_string(bundled_config_text())

    user_config = ensure_user_config_file(config_dir)
    config.read(user_config, encoding="utf-8")

    if cwd is not None:
        local_config = os.path.join(cwd, CONFIG_FILENAME)
        if os.path.exists(local_config):
            config.read(local_config, encoding="utf-8")

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
