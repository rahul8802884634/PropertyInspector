"""Open PropertyInspector and confirm it is in the foreground."""

from __future__ import annotations

from dataclasses import dataclass

from framework.core.config_reader import Settings
from framework.core.wait import WaitTimeout
from framework.pages.launch_page import LaunchPage


class AppLaunchError(Exception):
    """Raised when the app does not reach the foreground."""


@dataclass(frozen=True)
class LaunchResult:
    package: str
    activity: str


class AppLaunchFlow:
    def __init__(self, driver, settings: Settings):
        self.page = LaunchPage(driver, settings)
        self.settings = settings

    def execute(self) -> LaunchResult:
        self.page.activate()
        try:
            self.page.wait_until_launched()
        except WaitTimeout as exc:
            raise AppLaunchError(str(exc)) from exc

        return LaunchResult(
            package=self.page.current_package(),
            activity=self.page.current_activity(),
        )
