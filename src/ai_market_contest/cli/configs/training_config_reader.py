import pathlib
from ast import literal_eval
from configparser import ConfigParser
from typing import Any, Dict

from ai_market_contest.cli.configs.simulation_config_reader import (
    SimulationConfigReader,
)
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.environment import Market
from ai_market_contest.training.agent_name_maker import AgentNameMaker


class TrainingConfigReader(SimulationConfigReader):
    parsed_config: ConfigParser

    def get_self_play_num(self) -> int:
        return int(self.parsed_config["General"]["number_of_self_play_agents"])

    def get_num_agents(self) -> int:
        return self.get_self_play_num() + sum(self.get_naive_agent_counts().values())

    def get_other_config(self) -> Dict[str, Any]:
        return {
            setting_name: literal_eval(setting_value)
            for setting_name, setting_value in self.parsed_config["Other"].items()
        }

    def print_training(self) -> bool:
        # TODO add default value
        return bool(self.parsed_config["General"]["print_training"])

    def get_num_epochs(self) -> int:
        # TODO add default value
        return int(self.parsed_config["General"]["epochs"])
