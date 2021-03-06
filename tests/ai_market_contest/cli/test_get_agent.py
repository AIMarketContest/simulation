from ai_market_contest.cli.utils.agent_manipulation_utils import (
    create_custom_agent,
    remove_agent_dir,
)
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent
from ai_market_contest.cli.utils.get_agents import (
    add_trained_agent_to_config_file,
    get_agent_names,
    get_trained_agents,
)
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)


def test_get_agent_names(tmp_path):
    tmp_path = tmp_path / "aic"

    initialise_file_structure(tmp_path, ["test_author"])
    create_custom_agent(tmp_path, "test_agent")
    agent_names = get_agent_names(tmp_path)
    assert "test_agent" in agent_names

    create_custom_agent(tmp_path, "another_test_agent")
    agent_names = get_agent_names(tmp_path)
    assert "test_agent" in agent_names
    assert "another_test_agent" in agent_names

    remove_agent_dir("another_test_agent", tmp_path)
    agent_names = get_agent_names(tmp_path)
    assert "test_agent" in agent_names
    assert "another_test_agent" not in agent_names


def test_get_trained_agents(tmp_path):
    tmp_path = tmp_path / "aic"

    initialise_file_structure(tmp_path, ["test_author"])
    create_custom_agent(tmp_path, "test_agent")
    trained_agents = get_trained_agents(tmp_path / "agents/test_agent")

    assert trained_agents is not None


def test_get_trained_agents_info(tmp_path):
    tmp_path = tmp_path / "aic"

    initialise_file_structure(tmp_path, ["test_author"])
    create_custom_agent(tmp_path, "test_agent")
    trained_agents = get_trained_agents(tmp_path / "agents/test_agent")
    existing_agent = ExistingAgent("test_agent", tmp_path)
    trained_agents_info = existing_agent.get_trained_agents_info(trained_agents)

    assert trained_agents[0] in trained_agents_info.values()
    assert "Initial untrained agent" in list(trained_agents_info.keys())[0]


def test_add_trained_agent_to_config_file(tmp_path):
    tmp_path = tmp_path / "aic"

    initialise_file_structure(tmp_path, ["test_author"])
    create_custom_agent(tmp_path, "test_agent")
    add_trained_agent_to_config_file(
        tmp_path / "agents/test_agent", "some_hexidecimal_code_for_an_agent"
    )
    trained_agents = get_trained_agents(tmp_path / "agents/test_agent")

    assert "some_hexidecimal_code_for_an_agent" in trained_agents
