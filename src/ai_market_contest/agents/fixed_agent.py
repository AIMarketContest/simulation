from ai_market_contest.agent import Agent


class FixedAgent(Agent):
    """
    An agent that always returns the same price.
    """

    def __init__(self, price: int = 50):
        self.price = price

    def update(
        self,
        last_round_prices: list[float],
        last_round_sales: int,
        round_before_last_prices: list[float],
        round_before_last_sales: int,
        identity_index: int,
    ) -> None:
        pass

    def learning_has_converged(self):
        return True

    def policy(self, last_round_agents_prices: list[float], agent_index: int) -> float:
        return self.price

    def __str__(self):
        return f"FixedAgent(price: {self.price})"
