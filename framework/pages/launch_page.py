"""First screen after the app process comes to the foreground."""

from __future__ import annotations

from framework.core.config_reader import Settings
from framework.core.wait import wait_until
from framework.pages.base_page import BasePage


class LaunchPage(BasePage):
    def activate(self) -> None:
        self.driver.activate_app(self.settings.app_package)

    def current_package(self) -> str:
        return self.driver.current_package

    def current_activity(self) -> str:
        return getattr(self.driver, "current_activity", "") or ""

    def wait_until_launched(self) -> None:
        def is_ready() -> bool:
            if self.current_package() != self.settings.app_package:
                return False
            ready_id = self.settings.ready_accessibility_id
            if ready_id:
                self.find("accessibility id", ready_id)
            return True

        wait_until(
            is_ready,
            timeout=self.settings.timeout_seconds,
            interval=self.settings.poll_interval_seconds,
            message=f"{self.settings.app_package} did not finish launching",
        )
