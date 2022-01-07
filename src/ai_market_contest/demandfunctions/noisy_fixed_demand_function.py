from numpy.random import randint

from ai_market_contest.demand_function import DemandFunction
from typing import Dict

class NoisyFixedDemandFunction(DemandFunction):
    FIXED_QUANTITY: int = 1000

    def __init__(self):
        if self.FIXED_QUANTITY < 0:
            raise ValueError("fixed_quantity must be greater than or equal to 0")

    def get_sales(self, current_prices: Dict[str, int]) -> Dict[str, int]:
        return {
            agent: int(randint(0, 100) + self.FIXED_QUANTITY)
            for agent in current_prices.keys()
        }
