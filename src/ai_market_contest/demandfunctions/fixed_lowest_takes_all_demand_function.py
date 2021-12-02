import numpy as np

from ai_market_contest.demand_function import DemandFunction


class FixedLowestTakesAllDemandFunction(DemandFunction):
    """
    Demand function that gives all demand to the lowest price.

    Attributes
    ----------
    total_demand : int
        The total demand to be given at each time step.
    """

    def __init__(self, total_demand: int):
        self.total_demand: int = total_demand

    def get_sales(self, current_prices: list[float]) -> list[int]:
        lowest_index = np.argmin(current_prices)
        demands = len(current_prices) * [0]
        demands[lowest_index] = self.total_demand
        return demands

    def __str__(self):
        return f"FixedLowestTakesAllDemandFunction(total demand: {self.total_demand})"
