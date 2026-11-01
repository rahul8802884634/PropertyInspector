import pytest

from framework.core.config_reader import Settings, load_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()
