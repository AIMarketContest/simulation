from unittest import TestCase

from ai_market_contest.demand_function import DemandFunction
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction


class FixedDemandFunctionTest(TestCase):
    demand_function_with_quantity_of_four: DemandFunction = FixedDemandFunction(4)
    demand_function_with_quantity_of_six: DemandFunction = FixedDemandFunction(6)

    def test_function_returns_correct_number_of_demands(self):
        sales_with_four_prices: list[
            int
        ] = self.demand_function_with_quantity_of_four.get_sales([0.4, 0.3, 0.5, 0.5])
        assert len(sales_with_four_prices) == 4
        sales_with_three_prices: list[
            int
        ] = self.demand_function_with_quantity_of_four.get_sales([0.7, 0.3, 0.5])
        assert len(sales_with_three_prices) == 3

    def test_function_returns_fixed_quantity(self):
        assert self.demand_function_with_quantity_of_four.get_sales([0.5])[0] == 4

        assert self.demand_function_with_quantity_of_six.get_sales([0.3])[0] == 6

    def test_function_returns_list_with_only_same_element(self):
        assert (
            len(set(self.demand_function_with_quantity_of_four.get_sales([0.1, 0.2])))
            == 1
        )
        assert (
            len(set(self.demand_function_with_quantity_of_six.get_sales([0.1, 0.2])))
            == 1
        )
