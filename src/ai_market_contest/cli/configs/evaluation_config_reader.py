import pathlib
from configparser import ConfigParser

from ai_market_contest.cli.configs.simulation_config_reader import (
    SimulationConfigReader,
)
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator


class EvaluationConfigReader(SimulationConfigReader):
    def __init__(
        self,
        config_file_path: pathlib.Path,
        demand_function_locator: DemandFunctionLocator,
        agent_locator: AgentLocator,
        config_parser: ConfigParser = ConfigParser(),
    ):
        config_parser.optionxform = str
        super().__init__(
            config_file_path, demand_function_locator, agent_locator, config_parser
        )

    def get_num_agents(self) -> int:
        return (
            sum(self.get_naive_agent_counts().values())
            + sum(map(lambda x: x[1], self.get_trained_agent_counts().values()))
            + 1
        )
