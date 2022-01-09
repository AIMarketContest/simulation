import pathlib
import pickle
from typing import Any, Dict

from ray.rllib.policy.policy import PolicySpec

from ai_market_contest.cli.cli_config import MULTIAGENT_CONFIG_FILENAME
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.training.policy_selector import PolicySelector


class PolicyConfigMaker:
    def __init__(self, agent_locator: AgentLocator, policy_selector: PolicySelector):
        self.policy_selector: PolicySelector = policy_selector
        self.agent_locator: AgentLocator = agent_locator

    def get_policy_config(self) -> Dict[str, Dict[str, Any]]:
        agent_to_train: str = self.policy_selector.get_agent_name()
        policy_config: Dict[str, Dict[str, Any]] = {"multiagent": {}}
        policy_config["multiagent"]["policies_to_train"] = [agent_to_train]
        policy_config["multiagent"]["policies"] = {}
        policy_config["multiagent"]["policies"][agent_to_train] = PolicySpec(
            policy_class=self.agent_locator.get_agent(agent_to_train)
        )
        if self.policy_selector.has_self_play():
            agent_opponent: str = self.policy_selector.get_agent_opponent_name()
            policy_config["multiagent"]["policies"][agent_opponent] = PolicySpec(
                policy_class=self.agent_locator.get_agent(agent_opponent)
            )
        naive_agent: str
        for naive_agent in self.policy_selector.get_naive_agents_names():
            policy_config["multiagent"]["policies"][naive_agent] = PolicySpec(
                policy_class=self.agent_locator.get_agent(naive_agent)
            )
        policy_config["multiagent"][
            "policy_mapping_fn"
        ] = self.policy_selector.get_select_policy_function()
        self.policy_config = policy_config
        return policy_config

    def save_multiagent_config(self, agent_dir: pathlib.Path):
        multi_agent_config_file = agent_dir / MULTIAGENT_CONFIG_FILENAME
        with multi_agent_config_file.open("wb") as config_file:
            pickle.dump(config_file, self.policy_config)
