import pytest

from ai_market_contest.cli.cli import initialise_parser


@pytest.fixture
def parser():
    return initialise_parser()
