from configparser import ConfigParser
import pathlib
from ai_market_contest.cli.configs.simulation_config_reader import (
    SimulationConfigReader,
)
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator


class EvaluationConfigReader(SimulationConfigReader):
    def __init__(
        self,
        config_file_path: pathlib.Path,
        demand_function_locator: DemandFunctionLocator,
        config_parser: ConfigParser,
        num_trained_agents: int,
    ):
        super().__init__(config_file_path, demand_function_locator, config_parser)
        self.num_trained_agents = num_trained_agents

    def get_num_agents(self) -> int:
        return len(self.get_naive_agent_counts().values()) + self.num_trained_agents
