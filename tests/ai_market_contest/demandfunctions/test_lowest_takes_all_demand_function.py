from unittest import TestCase

from ai_market_contest.demand_function import DemandFunction
from ai_market_contest.demandfunctions.fixed_lowest_takes_all_demand_function import (
    LowestTakesAllDemandFunction,
)


class FixedDemandFunctionTest(TestCase):
    demand_function: DemandFunction = LowestTakesAllDemandFunction()

    def test_function_returns_correct_number_of_demands(self):
        sales_with_four_prices = self.demand_function.get_sales(
            {"agent_0": 10, "agent_1": 15, "agent_2": 13, "agent_3": 8}
        )
        assert len(sales_with_four_prices) == 4

        sales_with_three_prices = self.demand_function.get_sales(
            {"agent_0": 10, "agent_1": 15, "agent_2": 13}
        )
        assert len(sales_with_three_prices) == 3

    def test_function_returns_sales_only_for_lowest_seller(self):
        sales_with_four_prices = self.demand_function.get_sales(
            {"agent_0": 10, "agent_1": 15, "agent_2": 13, "agent_3": 8}
        )
        assert sales_with_four_prices["agent_0"] == 0
        assert sales_with_four_prices["agent_1"] == 0
        assert sales_with_four_prices["agent_2"] == 0
        assert sales_with_four_prices["agent_3"] == 1000

        sales_with_three_prices = self.demand_function.get_sales(
            {"agent_0": 10, "agent_1": 15, "agent_2": 13}
        )
        assert sales_with_three_prices["agent_0"] == 1000
        assert sales_with_three_prices["agent_1"] == 0
        assert sales_with_three_prices["agent_2"] == 0
