import pathlib
from ast import literal_eval
from configparser import ConfigParser
from typing import Any, Dict

from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
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

    def get_self_play_num(self) -> int:
        return int(self.parsed_config["General"]["number_of_self_play_agents"])

    def get_naive_agent_counts(self) -> Dict[str, int]:
        agent_name: str
        agent_count: str
        return {
            agent_name: int(agent_count)
            for agent_name, agent_count in self.parsed_config["Naive Agents"].items()
        }

    def get_num_agents(self) -> int:
        return self.get_self_play_num() + sum(self.get_naive_agent_counts().values())

    def get_other_config(self) -> Dict[str, Any]:
        return {
            setting_name: literal_eval(setting_value)
            for setting_name, setting_value in self.parsed_config["Other"].items()
        }

    def get_environment(self, agent_name_maker: AgentNameMaker) -> Market:
        return Market(
            self.get_num_agents(),
            self.demand_function_locator.get_demand_function(
                self.parsed_config["General"]["demand_function"]
            ),
            int(self.parsed_config["General"]["simulation_length"]),
            agent_name_maker,
        )

    def print_training(self) -> bool:
        # TODO add default value
        return bool(self.parsed_config["General"]["print_training"])

    def get_num_epochs(self) -> int:
        # TODO add default value
        return int(self.parsed_config["General"]["epochs"])

    def get_optimisation_algorithm(self) -> str:
        # Check optimisation algorithm is valid
        return self.parsed_config["General"]["optimisation_algorithm"]
