from configparser import ConfigParser

from importlib_metadata import pathlib

from ai_market_contest.cli.configs.evaluation_config_reader import (
    EvaluationConfigReader,
)
from ai_market_contest.cli.configs.simulation_config_reader import (
    SimulationConfigReader,
)
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)
from ai_market_contest.training.policy_config_maker import PolicyConfigMaker
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)
from src.ai_market_contest.training.training_config_maker import TrainingConfigMaker


def test_training_config(tmp_path):
    tmp_path = tmp_path / "aic"
    initialise_file_structure(tmp_path, ["TestAgent"], ["TestAuthor"])

    demand_function_locator = DemandFunctionLocator(tmp_path)
    config_parser = ConfigParser()
    config_parser.optionxform = str
    evaluation_config_reader = EvaluationConfigReader(
        tmp_path / "evaluation_configs/evaluation_example_config.ini",
        demand_function_locator,
        config_parser,
        0,
    )

    assert evaluation_config_reader.get_naive_agent_counts() == {
        "FixedFifty": 3,
        "Random": 1,
    }

    agent_name_maker = SequentialAgentNameMaker(4)
    market = evaluation_config_reader.get_environment(agent_name_maker)

    assert market.agents == ["player_0", "player_1", "player_2", "player_3"]
    assert market.simulation_length == 250
