import pathlib

from ai_market_contest.cli.utils.agent_manipulation_utils import (
    create_agent,
    remove_agent_dir,
)
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)


def test_create_agent(tmp_path: pathlib.Path):
    tmp_path = tmp_path / "aic"
    initialise_file_structure(tmp_path, ["test_agent"], ["test_author"])

    create_agent(tmp_path, "another_test_agent")

    agent_dir = tmp_path / "agents" / "another_test_agent"
    agent_file = agent_dir / "another_test_agent.py"

    assert agent_dir.exists()
    assert agent_file.exists()

    assert "class Another_test_Agent(Agent):" in agent_file.read_text()


def test_remove_agent(tmp_path: pathlib.Path):
    tmp_path = tmp_path / "aic"
    initialise_file_structure(tmp_path, ["test_agent"], ["test_author"])

    remove_agent_dir("test_agent", tmp_path)

    assert not (tmp_path / "agents" / "test_agent").exists()
