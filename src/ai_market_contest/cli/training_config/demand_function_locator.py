import pathlib

from ai_market_contest.demand_function import DemandFunction


class DemandFunctionLocator:
    def __init__(self, demand_function_path: pathlib.Path):
        self.demand_function_path: pathlib.Path = demand_function_path

    def get_demand_function(demand_function: str) -> DemandFunction:
        raise NotImplementedError()
