from numpy.random import randint

from ai_market_contest.demand_function import DemandFunction
from typing import Dict


class NoisyFixedDemandFunction(DemandFunction):
    def __init__(self, fixed_quantity: int = 1000):
        if fixed_quantity < 0:
            raise ValueError("fixed_quantity must be greater than or equal to 0")

        self.fixed_quantity: int = fixed_quantity

    def get_sales(self, current_prices: Dict[str, int]) -> Dict[str, int]:
        return {
            agent: int(randint(0, 100) + self.fixed_quantity)
            for agent in current_prices.keys()
        }
