from configparser import ConfigParser

from importlib_metadata import pathlib

from ai_market_contest.cli.utils.get_agents import get_trained_agents, get_trained_agents_info
from ai_market_contest.cli.utils.project_initialisation_utils import initialise_file_structure
from ai_market_contest.cli.utils.displayagents import (
    display_agents,
    display_training_configs,
    display_trained_agents
)

def test_display_agents(capsys, tmp_path):
    display_agents(["Agent1", "Agent2", "Agent3"])

    captured = capsys.readouterr()

    assert captured.out == "The current agents are: \n[Agent1, Agent2, Agent3]\n"

def test_display_trained_agents(capsys, tmp_path):
    tmp_path = tmp_path / "aic"

    initialise_file_structure(tmp_path, ["test_agent"], ["test_author"])
    trained_agents = get_trained_agents(tmp_path / "agents/test_agent")

    display_trained_agents(tmp_path / "agents/test_agent", trained_agents)
    trained_agents_info = get_trained_agents_info(
        trained_agents, tmp_path / "agents/test_agent"
    )
    captured = capsys.readouterr()

    assert captured.out == "\n0 " + list(trained_agents_info.keys())[0] + "\n"

