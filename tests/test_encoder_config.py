import textwrap

import pytest

from codix.encoder.config import load_encoder_config


def test_load_encoder_config_uses_bundled_defaults():
    config = load_encoder_config(
        required_sections=(
            "application",
            "infoframe",
            "playercontrol",
            "codingframework",
        )
    )

    assert config["application"]["cwd_file"] == "cwdfile.ini"
    assert config["application"]["default_cwd"] == "~"
    assert config["application"]["required_subfolders"] == "media,data"
    assert config["infoframe"]["background"] == "lightsteelblue"
    assert config["playercontrol"]["backend"] == "vlc"
    assert config["playercontrol"]["relief"] == "groove"
    assert config["codingframework"]["background"] == "palegoldenrod"


def test_load_encoder_config_allows_cwd_override(tmp_path):
    (tmp_path / "config.ini").write_text(
        textwrap.dedent(
            """
            [infoframe]
            background = plum
            """
        ),
        encoding="utf-8",
    )

    config = load_encoder_config(tmp_path, required_sections=("infoframe",))

    assert config["infoframe"]["background"] == "plum"
    assert config["infoframe"]["relief"] == "groove"


def test_load_encoder_config_allows_application_cwd_override(tmp_path):
    (tmp_path / "config.ini").write_text(
        textwrap.dedent(
            """
            [application]
            required_subfolders = media,data,exports
            """
        ),
        encoding="utf-8",
    )

    config = load_encoder_config(tmp_path, required_sections=("application",))

    assert config["application"]["required_subfolders"] == "media,data,exports"
    assert config["application"]["cwd_file"] == "cwdfile.ini"


def test_load_encoder_config_integer_options_are_available_as_ints():
    config = load_encoder_config(
        required_sections=("infoframe", "playercontrol", "codingframework")
    )

    assert config["infoframe"].getint("borderwidth") == 2
    assert config["infoframe"].getint("filename_width") == 30
    assert config["playercontrol"].getint("borderwidth") == 2
    assert config["codingframework"].getint("panel_max") == 5


def test_load_encoder_config_reports_missing_required_section():
    with pytest.raises(ValueError, match="Missing encoder config section: missing"):
        load_encoder_config(required_sections=("missing",))
