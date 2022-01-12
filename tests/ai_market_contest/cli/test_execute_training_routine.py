from ai_market_contest.cli.utils.agent_manipulation_utils import create_custom_agent
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgent,
)
from ai_market_contest.cli.utils.get_agents import get_trained_agents
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)


def test_set_up_and_execute_training_routine(tmp_path):
    tmp_path = tmp_path / "aic"
    initialise_file_structure(tmp_path, ["test_author"])
    create_custom_agent(tmp_path, "test_agent")
    agent = ExistingAgent("test_agent", tmp_path)
    trained_agent = get_trained_agents(tmp_path / "agents/test_agent")[0]
    # agent_version = ExistingAgentVersion(agent, trained_agent)

    # TODO :: figure out what arguments to put in here
    # set_up_and_execute_training_routine()

    # TODO :: Assertions
