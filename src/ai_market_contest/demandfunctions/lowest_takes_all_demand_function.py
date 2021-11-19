import numpy as np

from ai_market_contest.demand_function import DemandFunction


class LowestTakesAllDemandFunction(DemandFunction):
    """ """

    def __init__(self):
        pass

    def get_sales(self, current_prices: list[float]) -> list[int]:
        lowest_index = np.argmin(current_prices)
        demands = len(current_prices) * [0]
        demands[lowest_index] = 10
        return demands
