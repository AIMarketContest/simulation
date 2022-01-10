from ai_market_contest.cli.adddemandfunctionsubcommand import create_demand_function
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)


def test_get_demand_function(tmp_path):
    tmp_path = tmp_path / "aic"

    initialise_file_structure(tmp_path, ["TestAgent"], ["test_author"])
    create_demand_function(tmp_path, "ADemandFunction")

    demand_function_locator = DemandFunctionLocator(
        tmp_path / "environments/demandfunctions"
    )

    returned_demand_function = demand_function_locator.get_demand_function(
        "ADemandFunction"
    )
    assert returned_demand_function.__class__.__name__ == "ADemandFunction"

    try:
        demand_function_locator.get_demand_function("NotADemandFunction")
        assert False
    except Exception:
        assert True
