"""Create the Appium session used by every flow."""

from __future__ import annotations

from framework.core.config_reader import ConfigError, Settings


def create_driver(settings: Settings):
    """Start an Android session. The app opens from package/activity or app_path."""
    if settings.platform_name.lower() != "android":
        raise ConfigError(
            f"{settings.platform_name} is not wired up yet. Add it in framework/core/driver_factory.py."
        )

    from appium import webdriver
    from appium.options.android import UiAutomator2Options

    options = UiAutomator2Options()
    options.platform_name = settings.platform_name
    options.automation_name = settings.automation_name
    options.device_name = settings.device_name
    options.app_package = settings.app_package
    options.app_activity = settings.app_activity
    options.no_reset = settings.no_reset
    options.new_command_timeout = 120
    if settings.app_path:
        options.app = settings.app_path

    return webdriver.Remote(settings.server_url, options=options)
