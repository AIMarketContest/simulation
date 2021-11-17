import pytest
from cli import initialise_parser


@pytest.fixture
def parser():
    return initialise_parser()
