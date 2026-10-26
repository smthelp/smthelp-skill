"""Delivery sinks. A sink is upload(files: list[Path], folder_name: str, ucfg: dict, log) -> dict
returning at least {"location": str, "files": [{"name", "bytes"}]}. Register in SINKS."""
from . import local, gdrive_gws, rclone

SINKS = {"local": local.upload, "gdrive": gdrive_gws.upload, "rclone": rclone.upload}
