from statistics import NormalDist

from ai_market_contest.demand_function import DemandFunction


class GaussianDemandFunction(DemandFunction):
    """
    A demand function which determines the price using a Gaussian distribution.
    Attributes
    ----------
    max_sales_scale_factor: int
        A positive integer representing the quantity to be sold
        from an agent selling the product at price = 0.
    """

    def __init__(
        self, max_sales_scale_factor: int = 1000, mu: float = 0.5, sigma: float = 1.0
    ):
        """
        Parameters
        ----------
        max_scale_factor: int, default=1000
            A positive integer representing the quantity to be sold
            from an agent if there was no price competiton
            i.e. all agents set the same price.
        mu: float, default=0.5
            A number between 0 and 1 (inclusive) representing the mean
            price in the gaussian distribution model.
        sigma: float, default=1.0
            A positive number representing the standard deviation
            in the gaussian distribution model.
        Raises
        ______
        ValueError
            When scale_factor given is less than or equal to 0.
        """
        if max_sales_scale_factor <= 0:
            raise ValueError("max_sales_scale_factor must be greater than 0")
        if sigma <= 0:
            raise ValueError("sigma must be greater than 0")
        if not 0 <= mu <= 1:
            raise ValueError("mu must be between 0 and 1 (inclusive)")
        self.max_sales_scale_factor: int = max_sales_scale_factor
        self.mu: float = mu
        self.sigma: float = sigma

    def get_sales(self, current_prices: dict[str, int]) -> dict[str, int]:
        gaussian_distribution: "NormalDist" = NormalDist(mu=self.mu, sigma=self.sigma)

        sales: dict[str, int] = {}

        for agent, price in current_prices.items():
            sales[agent] = int(
                (1 - gaussian_distribution.cdf(price)) * self.max_sales_scale_factor
            )

        return sales
