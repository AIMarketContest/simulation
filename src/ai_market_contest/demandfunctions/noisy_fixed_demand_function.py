from numpy.random import randint

from ai_market_contest.demand_function import DemandFunction


class NoisyFixedDemandFunction(DemandFunction):
    """ """

    def __init__(self, fixed_quantity: int = 1):

        if fixed_quantity < 0:
            raise ValueError("fixed_quantity must be greater than or equal to 0")

        self.fixed_quantity: int = fixed_quantity

    def get_sales(self, current_prices: list[float]) -> list[int]:
        return [
            int(randint(0, 100) / 100.0 + self.fixed_quantity)
            for _ in range(len(current_prices))
        ]
