import pathlib
from ai_market_contest.cli.utils.get_agents import (
    get_agent_names,
    get_trained_agents,
    get_trained_agents_info,
    add_trained_agent_to_config_file
)

from ai_market_contest.cli.utils.agent_manipulation_utils import (
    remove_agent_dir,
    create_agent
)

from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)

from ai_market_contest.cli.utils.existing_agent.existing_agent_version import ExistingAgent
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import ExistingAgentVersion

from ai_market_contest.cli.utils.execute_training_routine import set_up_and_execute_training_routine, save_new_agent


def test_set_up_and_execute_training_routine(tmp_path):
    tmp_path = tmp_path / "aic"
    initialise_file_structure(tmp_path, ["test_agent"], ["test_author"])
    agent = ExistingAgent("test_agent", tmp_path)
    trained_agent = get_trained_agents(tmp_path / "agents/test_agent")[0]
    agent_version = ExistingAgentVersion(agent, trained_agent)

    # TODO :: figure out what arguments to put in here
    # set_up_and_execute_training_routine()

    # TODO :: Assertions