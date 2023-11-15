import importlib.util
import pathlib
from types import ModuleType

from ai_market_contest.cli.cli_config import (
    CUR_DEMAND_FUNCTIONS,
    DEMAND_FUNCTION_DIR_NAME,
    ENVS_DIR_NAME,
)
from ai_market_contest.demand_function import DemandFunction


class DemandFunctionLocator:
    def __init__(self, env_dir: pathlib.Path):
        self.env_dir = env_dir

    @staticmethod
    def from_path(path: str) -> "DemandFunctionLocator":
        demand_function_locator = DemandFunctionLocator(path / ENVS_DIR_NAME)
        return demand_function_locator

    def get_demand_function(self, demand_function_name: str) -> DemandFunction:
        if demand_function_name in CUR_DEMAND_FUNCTIONS:
            return CUR_DEMAND_FUNCTIONS[demand_function_name]()
        demand_function_file = (
            self.env_dir / DEMAND_FUNCTION_DIR_NAME / (demand_function_name + ".py")
        )
        spec = importlib.util.spec_from_file_location(
            demand_function_name, demand_function_file
        )
        if spec.loader is None:
            raise Exception("Error in finding the required demand function")
        demand_func_module: ModuleType = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(demand_func_module)  # type: ignore
        demand_function_cls = getattr(demand_func_module, demand_function_name)  # type: ignore
        return demand_function_cls()
