import copy
import pathlib
from configparser import ConfigParser

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import (
    AGENTS_DIR_NAME,
    CONFIG_FILENAME,
    ENVS_DIR_NAME,
)
from ai_market_contest.cli.configs.simulation_config_reader import (
    SimulationConfigReader,
)
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.config_utils import get_training_config_path
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)


class TrainingConfigReader(SimulationConfigReader):
    def __init__(
        self,
        config_file_path: pathlib.Path,
        demand_function_locator: DemandFunctionLocator,
        agent_locator: AgentLocator,
    ):
        super().__init__(
            config_file_path, demand_function_locator, agent_locator, ConfigParser()
        )

    @staticmethod
    def from_name(name: str, path: pathlib.Path):
        training_config_path: pathlib.Path = get_training_config_path(path, name)

        agent_locator: AgentLocator = AgentLocator.from_path(path)
        demand_function_locator: DemandFunctionLocator = (
            DemandFunctionLocator.from_path(path)
        )
        training_config = TrainingConfigReader(
            training_config_path, demand_function_locator, agent_locator
        )
        return training_config

    def get_self_play_num(self) -> int:
        return int(self.parsed_config["General"]["number_of_self_play_agents"])

    def get_self_play_agents(self, agent_version: ExistingAgentVersion) -> list[Agent]:
        agents: list[Agent] = []
        main_agent = self.agent_locator.get_agent_class_or_pickle(agent_version)

        for _ in range(self.get_self_play_num() + 1):
            agents.append(copy.deepcopy(main_agent))

        return agents

    def get_num_agents(self) -> int:
        return (
            self.get_self_play_num()
            + sum(self.get_naive_agent_counts().values())
            + sum(map(lambda x: x[1], self.get_trained_agent_counts().values()))
            + 1
        )

    def print_training(self) -> bool:
        if "print_training" not in self.parsed_config["General"]:
            return False

        # TODO add default value
        return bool(self.parsed_config["General"]["print_training"])

    def get_num_epochs(self) -> int:
        # TODO add default value
        return int(self.parsed_config["General"]["epochs"])

    def write_config_to_file(self, new_agent_dir: pathlib.Path):
        config_file: pathlib.Path = new_agent_dir / CONFIG_FILENAME
        with config_file.open("w") as cfg_file:
            self.parsed_config.write(cfg_file)
