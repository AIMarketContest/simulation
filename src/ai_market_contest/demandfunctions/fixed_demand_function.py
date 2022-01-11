from ai_market_contest.demand_function import DemandFunction


class FixedDemandFunction(DemandFunction):
    """
    A demand function which gives the same price every round.
    Attributes
    ----------
    fixed_quantity: int
        A positive integer representing the quantity to be purchased from each
        agent every round.
    """

    FIXED_QUANTITY: int = 1

    def __init__(self):
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

        if self.FIXED_QUANTITY < 0:
            raise ValueError("fixed_quantity must be greater than or equal to 0")

    def get_sales(self, current_prices: dict[str, int]) -> dict[str, int]:
        sales: dict[str, int] = {}

        for agent, _ in current_prices.items():
            sales[agent] = self.FIXED_QUANTITY

        return sales
