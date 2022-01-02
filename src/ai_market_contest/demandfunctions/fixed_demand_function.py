from ai_market_contest.demand_function import DemandFunction
from typing import Dict


class FixedDemandFunction(DemandFunction):
    """
    A demand function which gives the same price every round.
    Attributes
    ----------
    fixed_quantity: int
        A positive integer representing the quantity to be purchased from each
        agent every round.
    """

    def __init__(self, fixed_quantity: int = 1):
        """
        Parameters
        ----------
        fixed_quantity: int, default=1
            A positive integer representing the quantity to demand from each agent.
        Raises
        ______
        ValueError
            When quantity given is less than 0.
        """

        if fixed_quantity < 0:
            raise ValueError("fixed_quantity must be greater than or equal to 0")

        self.fixed_quantity: int = fixed_quantity

    def get_sales(self, current_prices: Dict[str, int]) -> Dict[str, int]:
        sales: Dict[str, int] = {}

        for agent, _ in current_prices.items():
            sales[agent] = self.fixed_quantity

        return sales
