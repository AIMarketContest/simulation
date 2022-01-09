from ai_market_contest.cli.initsubcommand import initialise_file_structure
from ai_market_contest.cli.adddemandfunctionsubcommand import (
    edit_environment_config_file,
    remove_demand_function,
    create_demand_function,
)


def test_create_demand_function(tmp_path):
    initialise_file_structure(tmp_path, ["test_agent"], ["test_author"])
    create_demand_function(tmp_path, "test_demand_function")

    demand_function_file = (
        tmp_path / "environments" / "demandfunctions" / "test_demand_function.py"
    )
    env_config_file = tmp_path / "environments" / "config.ini"

    assert demand_function_file.exists()
    assert (
        "class test_demand_function(metaclass=ABCMeta):"
        in demand_function_file.read_text()
    )
    assert "test_demand_function" in env_config_file.read_text()


def test_remove_demand_function(tmp_path):
    initialise_file_structure(tmp_path, ["test_agent"], ["test_author"])
    create_demand_function(tmp_path, "test_demand_function")
    demand_function_file = (
        tmp_path / "environments" / "demandfunctions" / "test_demand_function.py"
    )
    assert demand_function_file.exists()

    remove_demand_function("test_demand_function", tmp_path)
    assert not demand_function_file.exists()
