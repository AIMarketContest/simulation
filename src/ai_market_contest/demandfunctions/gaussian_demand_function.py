from statistics import NormalDist

import numpy as np

from ai_market_contest.demand_function import DemandFunction


class GaussianDemandFunction(DemandFunction):
    """
    A demand function which determines the price using a Gaussian distribution.
    Attributes
    ----------
    MAX_SALES_SCALE_FACTOR: int
        A positive integer representing the quantity to be sold
        from an agent selling the product at price = 0.
    """

    MAX_SALES_SCALE_FACTOR: int = 100
    MU: float = 50
    SIGMA: float = np.sqrt(sum(np.square(np.array([i for i in range(101)]) - MU)) / 100)

    def __init__(self):
        """
        Raises
        ______
        ValueError
            When scale_factor given is less than or equal to 0.
        """
        if self.MAX_SALES_SCALE_FACTOR <= 0:
            raise ValueError("max_sales_scale_factor must be greater than 0")
        if self.SIGMA <= 0:
            raise ValueError("sigma must be greater than 0")

    def get_sales(self, current_prices: dict[str, int]) -> dict[str, int]:
        gaussian_distribution: "NormalDist" = NormalDist(mu=self.MU, sigma=self.SIGMA)

        demand: dict[str, float] = {}
        total_demand = 0
        for agent, price in current_prices.items():
            demand[agent] = 1 - gaussian_distribution.cdf(price)
            total_demand += demand[agent]

        sales: dict[str, int] = {}
        for agent, price in current_prices.items():
            sales[agent] = int(
                self.MAX_SALES_SCALE_FACTOR * (demand[agent] / total_demand)
            )

        return sales
