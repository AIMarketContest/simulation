from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)


def test_get_agent(tmp_path):
    tmp_path = tmp_path / "aic"

    initialise_file_structure(tmp_path, ["TestAgent"], ["test_author"])
    agent_locator = AgentLocator(tmp_path / "agents")

    returned_agent = agent_locator.get_agent("TestAgent")
    assert returned_agent.__name__ == "TestAgent"

    returned_agent = agent_locator.get_agent("TestAgent-opponent")
    assert returned_agent.__name__ == "TestAgent"

    try:
        agent_locator.get_agent("NotAnAgent")
        assert False
    except Exception:
        assert True
