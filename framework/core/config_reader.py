"""Load framework settings from config/config.yaml and environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


class ConfigError(Exception):
    """Raised when required launch settings are missing or invalid."""


@dataclass(frozen=True)
class Settings:
    server_url: str
    platform_name: str
    automation_name: str
    device_name: str
    app_package: str
    app_activity: str
    app_path: str
    no_reset: bool
    timeout_seconds: float
    poll_interval_seconds: float
    ready_accessibility_id: str


def load_settings(path: Path | None = None) -> Settings:
    config_path = path or DEFAULT_CONFIG_PATH
    if not config_path.is_file():
        raise ConfigError(f"Config file not found: {config_path}")

    with config_path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    appium = raw.get("appium") or {}
    android = raw.get("android") or {}
    launch = raw.get("launch") or {}

    settings = Settings(
        server_url=_env("APPIUM_SERVER_URL", appium.get("server_url", "")),
        platform_name=_env("PLATFORM_NAME", android.get("platform_name", "Android")),
        automation_name=_env("AUTOMATION_NAME", android.get("automation_name", "UiAutomator2")),
        device_name=_env("ANDROID_DEVICE_NAME", android.get("device_name", "")),
        app_package=_env("APP_PACKAGE", android.get("app_package", "")),
        app_activity=_env("APP_ACTIVITY", android.get("app_activity", "")),
        app_path=_env("APP_PATH", android.get("app_path", "")),
        no_reset=_as_bool(_env("NO_RESET", android.get("no_reset", False))),
        timeout_seconds=float(_env("LAUNCH_TIMEOUT_SECONDS", launch.get("timeout_seconds", 30))),
        poll_interval_seconds=float(
            _env("LAUNCH_POLL_INTERVAL_SECONDS", launch.get("poll_interval_seconds", 0.5))
        ),
        ready_accessibility_id=_env(
            "LAUNCH_READY_ACCESSIBILITY_ID", launch.get("ready_accessibility_id", "")
        ),
    )
    _validate(settings)
    return settings


def _env(name: str, fallback):
    value = os.environ.get(name)
    if value is None or value == "":
        return fallback
    return value


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _validate(settings: Settings) -> None:
    missing = [
        name
        for name, value in (
            ("appium.server_url", settings.server_url),
            ("android.device_name", settings.device_name),
            ("android.app_package", settings.app_package),
            ("android.app_activity", settings.app_activity),
        )
        if not str(value).strip()
    ]
    if missing:
        raise ConfigError("Missing required settings: " + ", ".join(missing))
    if settings.timeout_seconds <= 0:
        raise ConfigError("launch.timeout_seconds must be greater than 0")
    if settings.poll_interval_seconds <= 0:
        raise ConfigError("launch.poll_interval_seconds must be greater than 0")
