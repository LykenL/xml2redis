import os

import pytest

from app.parser import parse_config

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture
def config_path():
    return os.path.join(FIXTURES, "config.xml")


@pytest.fixture
def real_config(config_path):
    """Parsed version of the config.xml that ships with the task."""
    return parse_config(config_path)


@pytest.fixture
def minimal_path():
    return os.path.join(FIXTURES, "minimal.xml")
