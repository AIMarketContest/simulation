import pathlib

from ai_market_contest.cli.adddemandfunctionsubcommand import (
    create_demand_function,
    remove_demand_function,
)
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)


def test_create_demand_function(tmp_path: pathlib.Path):
    tmp_path = tmp_path / "aic"
    initialise_file_structure(tmp_path, ["test_author"])

    create_demand_function(tmp_path, "test_demand_function")

    demand_function_file = (
        tmp_path / "environments" / "demandfunctions" / "test_demand_function.py"
    )
    env_config_file = tmp_path / "environments" / "config.ini"

    assert demand_function_file.exists()
    assert (
        "class test_demand_function(DemandFunction):"
        in demand_function_file.read_text()
    )
    assert "test_demand_function" in env_config_file.read_text()


def test_remove_demand_function(tmp_path: pathlib.Path):
    initialise_file_structure(tmp_path, ["test_author"])
    create_demand_function(tmp_path, "test_demand_function")
    demand_function_file = (
        tmp_path / "environments" / "demandfunctions" / "test_demand_function.py"
    )
    assert demand_function_file.exists()

    # TODO :: Uncomment this line once the function compiles
    remove_demand_function("test_demand_function", tmp_path)
    assert not demand_function_file.exists()
