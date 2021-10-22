from demand_function import DemandFunction
from statistics import NormalDist


class GaussianDemandFunction(DemandFunction):
    """
    A demand function which determines the price using a Gaussian distribution.

    Attributes
    ----------
    max_sales_scale_factor: int
        A positive integer representing the quantity to be sold
        from an agent selling the product at price = 0

    """

    def __init__(self, max_sales_scale_factor: int = 1000):
        """
        Parameters
        ----------
        max_scale_factor: int, default=1000
            A positive integer representing the quantity to be sold
            from an agent if there was no price competiton
            i.e. all agents set the same price

        Raises
        ______
        ValueError
            When scale_factor given is less than or equal to 0.
        """

        if max_sales_scale_factor <= 0:
            raise ValueError("max_sales_scale_factor must be greater than 0")
        self.max_sales_scale_factor = max_sales_scale_factor

    def get_sales(self, current_prices: list[float]) -> list[int]:

        N: int = len(current_prices)
        gaussian_distribution: "NormalDist" = NormalDist(mu=0.5, sigma=1)
        return [
            int((1 - gaussian_distribution.cdf(price)) * self.max_sales_scale_factor)
            for price in current_prices
        ]
