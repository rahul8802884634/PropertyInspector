from pathlib import Path

import pytest

from framework.core.config_reader import ConfigError, load_settings


def test_load_settings_reads_yaml_and_env(tmp_path: Path, monkeypatch):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
appium:
  server_url: http://127.0.0.1:4723
android:
  platform_name: Android
  automation_name: UiAutomator2
  device_name: Pixel
  app_package: com.example.app
  app_activity: .MainActivity
  app_path: ""
  no_reset: false
launch:
  timeout_seconds: 10
  poll_interval_seconds: 0.2
  ready_accessibility_id: ""
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("APP_PACKAGE", "com.propertyinspector")
    monkeypatch.setenv("NO_RESET", "true")

    settings = load_settings(config_file)

    assert settings.app_package == "com.propertyinspector"
    assert settings.no_reset is True
    assert settings.device_name == "Pixel"
    assert settings.timeout_seconds == 10


def test_load_settings_rejects_a_missing_package(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("APP_PACKAGE", raising=False)
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
appium:
  server_url: http://127.0.0.1:4723
android:
  device_name: Pixel
  app_package: ""
  app_activity: .MainActivity
launch:
  timeout_seconds: 5
  poll_interval_seconds: 0.1
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="app_package"):
        load_settings(config_file)
