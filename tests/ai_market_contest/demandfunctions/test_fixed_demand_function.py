from unittest import TestCase

from ai_market_contest.demand_function import DemandFunction
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction


class FixedDemandFunctionTest(TestCase):
    demand_function: DemandFunction = FixedDemandFunction()

    def test_function_returns_correct_number_of_demands(self):
        sales_with_four_prices = self.demand_function.get_sales(
            {"agent_0": 10, "agent_1": 15, "agent_2": 10, "agent_3": 8}
        )
        assert len(sales_with_four_prices) == 4
        sales_with_three_prices = self.demand_function.get_sales(
            {"agent_0": 10, "agent_1": 15, "agent_2": 10}
        )
        assert len(sales_with_three_prices) == 3

    def test_function_returns_single_sale(self):
        assert self.demand_function.get_sales({"agent": 10})["agent"] == 1
