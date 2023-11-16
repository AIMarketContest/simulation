from configparser import ConfigParser

from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)


def test_training_config(tmp_path):
    tmp_path = tmp_path / "aic"
    initialise_file_structure(tmp_path, ["TestAuthor"])

    demand_function_locator = DemandFunctionLocator(tmp_path)
    config_parser = ConfigParser()
    config_parser.optionxform = str
    training_config_reader = TrainingConfigReader(
        tmp_path / "training_configs/training_example_config.ini",
        demand_function_locator,
        config_parser,
    )

    assert training_config_reader.get_naive_agent_counts() == {
        "FixedFifty": 3,
        "Random": 1,
    }
    assert training_config_reader.get_other_config() == {"num_workers": 4}
    assert training_config_reader.get_num_epochs() == 20
    assert not training_config_reader.print_training()

    agent_name_maker = SequentialAgentNameMaker(4)
    market = training_config_reader.get_environment(agent_name_maker)

    assert market.agents == ["player_0", "player_1", "player_2", "player_3"]
    assert market.simulation_length == 200

    training_config_reader.write_config_to_file(tmp_path / "training_configs")
    assert (tmp_path / "training_configs/config.ini").exists()
