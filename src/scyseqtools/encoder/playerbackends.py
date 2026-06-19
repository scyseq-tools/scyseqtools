"""Media-player backends for the encoder player control."""

import time


DEFAULT_BACKEND = "vlc"
SUPPORTED_BACKENDS = ("vlc", "mpv")


class PlayerBackendError(RuntimeError):
    """Raised when a configured media-player backend cannot be used."""


def normalize_backend_name(name):
    """Return a supported backend name from config/user input."""
    backend_name = (name or DEFAULT_BACKEND).strip().lower()
    if backend_name not in SUPPORTED_BACKENDS:
        names = ", ".join(SUPPORTED_BACKENDS)
        raise PlayerBackendError(
            f"Unsupported media player backend '{backend_name}'. "
            f"Use one of: {names}."
        )
    return backend_name


def configured_backend_name(playercontrol_config):
    """Return the configured backend name from the playercontrol section."""
    return normalize_backend_name(playercontrol_config.get("backend", DEFAULT_BACKEND))


def create_player_backend(name, file_name):
    """Create the configured media-player backend."""
    backend_name = normalize_backend_name(name)
    if backend_name == "vlc":
        return VlcPlayerBackend(file_name)
    if backend_name == "mpv":
        return MpvPlayerBackend(file_name)
    raise AssertionError(f"Unhandled media player backend: {backend_name}")


class VlcPlayerBackend:
    """VLC implementation of the media-player backend API."""

    def __init__(self, file_name):
        try:
            import vlc
        except ImportError as exc:
            raise PlayerBackendError(
                "The VLC backend requires the python-vlc package and VLC 64-bit."
            ) from exc

        args = ["--no-xlib"]
        instance = vlc.Instance(args)
        self._player = instance.media_player_new()
        self.load(file_name)

    def load(self, file_name):
        self._player.set_mrl(file_name)
        # Warm VLC up so duration and audio initialization are available.
        self._player.play()
        time.sleep(1)
        self.pause()

    def play(self):
        self._player.play()

    def pause(self):
        self._player.set_pause(do_pause=1)

    def get_time(self):
        return self._player.get_time()

    def set_time(self, value):
        self._player.set_time(value)

    def get_length(self):
        return self._player.get_length()


class MpvPlayerBackend:
    """MPV implementation of the media-player backend API."""

    def __init__(self, file_name):
        try:
            import mpv
        except ImportError as exc:
            raise PlayerBackendError(
                "The MPV backend requires the optional 'mpv' Python package "
                "and system libmpv. Install with 'pip install scyseqtools[mpv]' "
                "or 'pip install mpv', and make sure libmpv is available."
            ) from exc

        player_factory = getattr(mpv, "MPV", None) or getattr(mpv, "Mpv", None)
        if player_factory is None:
            raise PlayerBackendError(
                "The MPV backend could not find python-mpv's MPV class."
            )

        try:
            self._player = player_factory()
            initialize = getattr(self._player, "initialize", None)
            if callable(initialize):
                initialize()
        except Exception as exc:
            raise PlayerBackendError(
                "The MPV backend could not start. Make sure system libmpv is "
                "installed and visible in PATH."
            ) from exc

        self.load(file_name)

    def load(self, file_name):
        self._player.pause = True
        self._player.play(file_name)
        self._wait_for_duration()

    def play(self):
        self._player.pause = False

    def pause(self):
        self._player.pause = True

    def get_time(self):
        time_pos = getattr(self._player, "time_pos", None)
        if time_pos is None:
            time_pos = getattr(self._player, "playback_time", None)
        if time_pos is None:
            return -1
        return int(round(time_pos * 1000))

    def set_time(self, value):
        self._player.command("seek", value / 1000.0, "absolute+exact")

    def get_length(self):
        duration = getattr(self._player, "duration", None)
        if duration is None:
            return -1
        return int(round(duration * 1000))

    def _wait_for_duration(self, attempts=10, delay=0.1):
        for _ in range(attempts):
            if self.get_length() > 0:
                break
            time.sleep(delay)
