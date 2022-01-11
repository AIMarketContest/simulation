import pathlib

from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)
from ai_market_contest.training.policy_config_maker import PolicyConfigMaker
from ai_market_contest.training.policy_selector import PolicySelector


def test_policy_config_maker(tmp_path: pathlib.Path):
    tmp_path = tmp_path / "aic"
    initialise_file_structure(tmp_path, ["TestAgent"], ["TestAuthor"])

    agent_locator = AgentLocator(tmp_path / "agents")
    policy_selector = PolicySelector(agent_name="TestAgent", self_play_number=1)
    policy_config_maker = PolicyConfigMaker(agent_locator, policy_selector)

    res = policy_config_maker.get_policy_config()

    assert "multiagent" in res
    multiagent = res["multiagent"]
    assert "policies_to_train" in multiagent
    assert "policies" in multiagent
    assert "policy_mapping_fn" in multiagent
    assert "TestAgent" in multiagent["policies"]
    assert multiagent["policies"]["TestAgent"][0].__name__ == "TestAgent"
    assert "TestAgent-opponent" in multiagent["policies"]
    assert multiagent["policies"]["TestAgent-opponent"][0].__name__ == "TestAgent"
