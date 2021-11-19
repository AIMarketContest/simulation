import pytest

from ai_market_contest.cli.cli import initialise_parser  # type: ignore


@pytest.fixture
def parser():
    return initialise_parser()
