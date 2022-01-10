from statistics import NormalDist
from typing import Dict

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

    MAX_SALES_SCALE_FACTOR: int = 1000
    MU: float = 0
    SIGMA: float = 1

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
        if not 0 <= self.MU <= 1:
            raise ValueError("mu must be between 0 and 1 (inclusive)")

    def get_sales(self, current_prices: dict[str, int]) -> dict[str, int]:
        gaussian_distribution: "NormalDist" = NormalDist(mu=self.MU, sigma=self.SIGMA)

        sales: dict[str, int] = {}

        for agent, price in current_prices.items():
            sales[agent] = int(
                (1 - gaussian_distribution.cdf(price)) * self.MAX_SALES_SCALE_FACTOR
            )

        return sales
