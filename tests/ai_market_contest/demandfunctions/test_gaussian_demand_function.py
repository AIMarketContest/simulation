from unittest import TestCase

from demand_function import DemandFunction
from demandfunctions.gaussian_demand_function import GaussianDemandFunction


class GaussianDemandFunctionTest(TestCase):
    demand_function_with_default_sf: DemandFunction = GaussianDemandFunction()
    demand_function_with_sf_ten: DemandFunction = GaussianDemandFunction(10)

    def test_function_returns_correct_number_of_demands(self):
        sales_with_four_prices: list[
            int
        ] = self.demand_function_with_default_sf.get_sales(
            [0.4, 0.3, 0.5, 0.5]
        )
        assert len(sales_with_four_prices) == 4
        sales_with_three_prices: list[
            int
        ] = self.demand_function_with_default_sf.get_sales([0.7, 0.3, 0.5])
        assert len(sales_with_three_prices) == 3

    def test_function_returns_gaussian_(self):
        assert self.demand_function_with_default_sf.get_sales([0.5])[0] == 500

        assert self.demand_function_with_sf_ten.get_sales([0.3])[0] == 5
