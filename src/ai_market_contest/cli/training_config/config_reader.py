import pathlib
from configparser import ConfigParser
from typing import Dict

from ai_market_contest.demand_function import DemandFunction
from ai_market_contest.cli.training_config.demand_function_locator import (
    DemandFunctionLocator,
)
from ai_market_contest.environment import Market
from ai_market_contest.training.agent_name_maker import AgentNameMaker


class TrainingConfigReader:
    parsed_config: ConfigParser

    def __init__(
        self,
        config_file_path: pathlib.Path,
        demand_function_locator: DemandFunctionLocator = None,
        config_parser: ConfigParser = ConfigParser(),
    ):
        config_parser.read(config_file_path)
        self.parsed_config: ConfigParser = config_parser
        self.demand_function_locator: DemandFunctionLocator = demand_function_locator

    def get_naive_agent_nums(self) -> Dict[str, str]:
        return self.parsed_config["Naive Agents"]

    def get_num_agents(self) -> int:
        return (
            int(self.parsed_config["General"]["number_of_self_play_agents"])
            + int(len(self.parsed_config["Naive Agents"].keys()))
        )

    def get_other_config(self) -> Dict[str, str]:
        return self.parsed_config["Other"]

    def get_environment(self, agent_name_maker: AgentNameMaker) -> Market:
        return Market(
            self.get_num_agents(),
            self.demand_function_locator.get_demand_function(self.parsed_config[
                "General"
            ]["demand_function"]),
            self.parsed_config["General"]["training_duration"],
            agent_name_maker
        )