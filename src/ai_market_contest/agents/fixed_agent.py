from agent import Agent


class FixedAgent(Agent):
    """
    An agent that always returns the same price.
    """

    def __init__(self, price: float = 0.5):
        if not 0 <= price <= 1:
            raise ValueError("Price must be between 0 and 1")

        self.price = price

    def update(
            self,
            last_round_agents_prices: list[float],
            last_round_sales: int,
            identity_index: int
    ) -> None:
        pass

    def policy(self) -> float:
        return self.price
