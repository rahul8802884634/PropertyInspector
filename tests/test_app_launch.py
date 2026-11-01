"""Launch flow checks. Device test stays off unless you opt in."""

import pytest

from framework.core.config_reader import Settings
from framework.core.driver_factory import create_driver
from framework.flows.app_launch_flow import AppLaunchError, AppLaunchFlow


class FakeDriver:
    def __init__(self, package: str, activity: str = ".MainActivity", fail_lookups: int = 0):
        self.package = package
        self.activity = activity
        self.fail_lookups = fail_lookups
        self.activated: list[str] = []
        self.lookups: list[tuple[str, str]] = []

    def activate_app(self, app_id: str) -> None:
        self.activated.append(app_id)
        self.package = app_id

    @property
    def current_package(self) -> str:
        return self.package

    @property
    def current_activity(self) -> str:
        return self.activity

    def find_element(self, strategy: str, value: str):
        self.lookups.append((strategy, value))
        if self.fail_lookups > 0:
            self.fail_lookups -= 1
            raise RuntimeError("element not on screen yet")
        return object()


def _settings(**overrides) -> Settings:
    values = dict(
        server_url="http://127.0.0.1:4723",
        platform_name="Android",
        automation_name="UiAutomator2",
        device_name="Pixel",
        app_package="com.propertyinspector",
        app_activity=".MainActivity",
        app_path="",
        no_reset=False,
        timeout_seconds=0.4,
        poll_interval_seconds=0.01,
        ready_accessibility_id="",
    )
    values.update(overrides)
    return Settings(**values)


def test_launch_flow_brings_the_app_to_the_foreground():
    settings = _settings()
    driver = FakeDriver(package="com.android.launcher")

    result = AppLaunchFlow(driver, settings).execute()

    assert driver.activated == ["com.propertyinspector"]
    assert result.package == "com.propertyinspector"
    assert result.activity == ".MainActivity"


def test_launch_flow_fails_when_another_app_stays_in_front():
    settings = _settings()
    driver = FakeDriver(package="com.android.settings")
    driver.activate_app = lambda app_id: None  # type: ignore[method-assign]

    with pytest.raises(AppLaunchError, match="com.propertyinspector"):
        AppLaunchFlow(driver, settings).execute()


def test_launch_flow_waits_for_the_ready_element():
    settings = _settings(ready_accessibility_id="home_screen")
    driver = FakeDriver(package="com.android.launcher", fail_lookups=1)

    result = AppLaunchFlow(driver, settings).execute()

    assert result.package == "com.propertyinspector"
    assert driver.lookups == [("accessibility id", "home_screen"), ("accessibility id", "home_screen")]


@pytest.mark.device
def test_app_launches_on_device(settings):
    driver = create_driver(settings)
    try:
        result = AppLaunchFlow(driver, settings).execute()
        assert result.package == settings.app_package
    finally:
        driver.quit()
