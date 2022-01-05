from typing import Dict, List

from ray.rllib.policy.policy import PolicySpec

from ai_market_contest.cli.utils.agentlocator import AgentLocator
from ai_market_contest.training.policy_selector import PolicySelector


class PolicyConfigMaker:
    def __init__(self, agent_locator: AgentLocator, policy_selector: PolicySelector):
        self.policy_selector = policy_selector
        self.agent_locator = agent_locator

    def get_policy_config(self):
        agent_to_train = self.policy_selector.get_agent_name()
        policy_config = {"multiagent": {}}
        policy_config["multiagent"]["policies_to_train"] = [agent_to_train_str]
        policy_config["multiagent"]["policies"] = {}
        policy_config["multiagent"]["policies"][agent_to_train] = PolicySpec(
            policy_class=agentlocator.get_agent(agent_to_train)
        )
        if self.policy_selector.has_self_play():
            agent_opponent = self.policy_selector.get_agent_opponent_name()
            policy_config["multiagent"]["policies"][agent_opponent] = PolicySpec(
                policy_class=agentlocator.get_agent(agent_opponent)
            )
        for naive_agent in self.policy_selector.get_naive_agents_names():
            policy_config["multiagent"]["policies"][naive_agent] = PolicySpec(
                policy_class=agentlocator.get_agent(naive_agent)
            )
        policy_config["multiagent"][
            "policy_mapping_fn"
        ] = self.policy_selector.get_select_policy_function()
        return policy_config
