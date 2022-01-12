from ast import literal_eval
import pathlib
from configparser import ConfigParser
from typing import Dict, Tuple

from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.environment import Market
from ai_market_contest.training.agent_name_maker import AgentNameMaker


class SimulationConfigReader:
    def __init__(
        self,
        config_file_path: pathlib.Path,
        demand_function_locator: DemandFunctionLocator,
        config_parser: ConfigParser = ConfigParser(),
    ):
        config_parser.optionxform = str
        config_parser.read(config_file_path)
        self.parsed_config: ConfigParser = config_parser
        self.demand_function_locator: DemandFunctionLocator = demand_function_locator

    def get_naive_agent_counts(self) -> dict[str, int]:
        if "Naive Agents" not in self.parsed_config:
            return {}

        return {
            agent_name: int(agent_count)
            for agent_name, agent_count in self.parsed_config["Naive Agents"].items()
        }

    def get_trained_agent_counts(self) -> Dict[str, Tuple[str, int]]:
        if "Trained Agents" not in self.parsed_config:
            return {}
        return {
            agent_name: literal_eval(hash_and_num)
            for agent_name, hash_and_num in self.parsed_config["Trained Agents"].items()
        }

    def get_epochs(self) -> int:
        return int(self.parsed_config["General"]["epochs"])

    def get_num_agents(self) -> int:
        raise NotImplementedError("Must be implemented by a subclass")

    def get_environment(self, agent_name_maker: AgentNameMaker) -> Market:
        return Market(
            self.get_num_agents(),
            self.demand_function_locator.get_demand_function(
                self.parsed_config["General"]["demand_function"]
            ),
            int(self.parsed_config["General"]["simulation_length"]),
            agent_name_maker,
        )

    def get_optimisation_algorithm(self) -> str:
        # TODO: Check optimisation algorithm is valid
        return self.parsed_config["General"]["optimisation_algorithm"]
