from agent import Agent


class ZeroAgent(Agent):
    """
    An agent that always returns a price of 0.
    """

    def get_initial_price(self) -> float:
        return 0

    def get_price(
        self,
        last_round_agents_prices: list[float],
        last_round_sales: int,
        identity_index: int,
    ) -> float:
        return 0
