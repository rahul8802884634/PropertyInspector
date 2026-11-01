"""Small poll helper used by page objects."""

from __future__ import annotations

import time


class WaitTimeout(TimeoutError):
    """Raised when a screen condition is not met in time."""


def wait_until(predicate, timeout: float, interval: float, message: str) -> None:
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None

    while True:
        try:
            if predicate():
                return
        except Exception as exc:  # locator lookups fail until the screen is ready
            last_error = exc

        if time.monotonic() >= deadline:
            raise WaitTimeout(message) from last_error
        time.sleep(interval)
