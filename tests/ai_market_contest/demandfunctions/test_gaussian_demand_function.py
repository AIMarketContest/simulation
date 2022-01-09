from unittest import TestCase

from ai_market_contest.demand_function import DemandFunction
from ai_market_contest.demandfunctions.gaussian_demand_function import (
    GaussianDemandFunction,
)


class GaussianDemandFunctionTest(TestCase):
    demand_function_with_default_sf: DemandFunction = GaussianDemandFunction()
    demand_function_with_sf_ten: DemandFunction = GaussianDemandFunction()

    def test_function_returns_correct_number_of_demands(self):
        sales_with_four_prices: list[
            int
        ] = self.demand_function_with_default_sf.get_sales(
            {"agent_0": 10, "agent_1": 15, "agent_2": 10, "agent_3": 8}
        )
        assert len(sales_with_four_prices) == 4
        sales_with_three_prices: list[
            int
        ] = self.demand_function_with_default_sf.get_sales(
            {"agent_0": 10, "agent_1": 15, "agent_2": 10}
        )
        assert len(sales_with_three_prices) == 3

    def test_function_returns_gaussian_(self):
        assert (
            self.demand_function_with_default_sf.get_sales({"agent_0": 0.5})["agent_0"]
            == 308
        )

        assert (
            self.demand_function_with_sf_ten.get_sales({"agent_0": 0.3})["agent_0"]
            == 382
        )
