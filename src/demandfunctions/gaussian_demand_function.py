from demand_function import DemandFunction
from scipy.stats import norm


class GaussianDemandFunction(DemandFunction):
    
    def __init__(self, max_sales_scale_factor: int = 1000):
        self.max_sales_scale_factor = max_sales_scale_factor

    def get_sales(self, current_prices: list[float]) -> list[int]:
        N: int = len(current_prices)
        mean: float = sum(current_prices) / N
        standard_deviation: float = sum(
            map(lambda x: pow(x, 2), current_prices)
        ) / N - pow(mean, 2)
        gaussian_distribution : 'norm' = norm(mean, standard_deviation)
        return [
            int((1 - gaussian_distribution.cdf(price)) * self.max_sales_scale_factor)
            for price in current_prices
        ]
