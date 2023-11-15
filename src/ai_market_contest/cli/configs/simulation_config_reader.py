import copy
import pathlib
from ast import literal_eval
from configparser import ConfigParser
from typing import Any, Union

import gym
from ray.rllib.agents.trainer import Trainer

from ai_market_contest.agent import Agent
from ai_market_contest.cli.configs.agent_config_reader import AgentConfigReader
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.demand_function import DemandFunction
from ai_market_contest.environment import Market
from ai_market_contest.training.agent_name_maker import AgentNameMaker


class SimulationConfigReader:
    def __init__(
        self,
        config_file_path: pathlib.Path,
        demand_function_locator: DemandFunctionLocator,
        agent_locator: AgentLocator,
        config_parser: ConfigParser = ConfigParser(),
    ):
        self.config_file_path = config_file_path
        config_parser.optionxform = str
        config_parser.read(config_file_path)
        self.parsed_config: ConfigParser = config_parser
        self.demand_function_locator = demand_function_locator
        self.agent_locator = agent_locator

    def get_naive_agent_counts(self) -> dict[str, int]:
        if "Naive Agents" not in self.parsed_config:
            return {}

        return {
            agent_name: int(agent_count)
            for agent_name, agent_count in self.parsed_config["Naive Agents"].items()
        }

    def get_trained_agent_counts(self) -> dict[str, tuple[str, int]]:
        if "Trained Agents" not in self.parsed_config:
            return {}
        return {
            agent_name: literal_eval(hash_and_num)
            for agent_name, hash_and_num in self.parsed_config["Trained Agents"].items()
        }

    def get_naive_agents(self) -> list[Agent]:
        agents: list[Agent] = []
        for agent_name, num in self.get_naive_agent_counts().items():
            agent = self.agent_locator.get_agent(agent_name)
            for _ in range(int(num)):
                agents.append(copy.deepcopy(agent()))

        return agents

    def get_trained_agents(
        self,
        proj_dir: pathlib.Path,
        env: gym.Env,
    ) -> list[Union[Agent, Trainer]]:
        agents: list[Union[Agent, Trainer]] = []
        for agent_name, (agent_hash, num) in self.get_trained_agent_counts().items():
            trained_exisiting_agent = ExistingAgent(agent_name, proj_dir)
            trained_agent_version = ExistingAgentVersion(
                trained_exisiting_agent, agent_hash
            )
            agent_config_reader: AgentConfigReader = AgentConfigReader(
                trained_agent_version
            )
            if agent_config_reader.get_agent_type() == "rllib":
                agent = self.agent_locator.get_trainer(
                    trained_agent_version,
                    env,
                    agent_config_reader,
                    self.get_other_config(),
                )
            else:
                agent = self.agent_locator.get_agent_class_or_pickle(
                    trained_agent_version
                )

            if num == 1:
                agents.append(agent)
            else:
                for _ in range(num):
                    agents.append(copy.deepcopy(agent))

        return agents

    def get_other_config(self) -> dict[str, Any]:
        return {
            setting_name: literal_eval(setting_value)
            for setting_name, setting_value in self.parsed_config["Other"].items()
        }

    def get_epochs(self) -> int:
        return int(self.parsed_config["General"]["epochs"])

    def get_num_agents(self) -> int:
        raise NotImplementedError("Must be implemented by a subclass")

    def get_simulation_length(self) -> int:
        return int(self.parsed_config["General"]["simulation_length"])

    def get_demand_function_name(self) -> str:
        return self.parsed_config["General"]["demand_function"]

    def get_environment(self, agent_name_maker: AgentNameMaker) -> Market:
        demand_function_name: str = self.get_demand_function_name()
        demand_function: DemandFunction = (
            self.demand_function_locator.get_demand_function(demand_function_name)
        )

        return Market(
            demand_function,
            self.get_simulation_length(),
            agent_name_maker,
        )

    def get_config_file_path(self) -> pathlib.Path:
        return self.config_file_path
