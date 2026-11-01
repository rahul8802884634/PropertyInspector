"""Actions shared by every screen."""

from __future__ import annotations

from framework.core.config_reader import Settings


class BasePage:
    def __init__(self, driver, settings: Settings):
        self.driver = driver
        self.settings = settings

    def find(self, strategy: str, value: str):
        return self.driver.find_element(strategy, value)
