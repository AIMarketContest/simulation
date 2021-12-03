import random

from ai_market_contest.agent import Agent


class RandomAgent(Agent):
    """
    An agent which returns a random price.
    """

    def update(
        self,
        last_round_prices: list[float],
        last_round_sales: int,
        round_before_last_prices: list[float],
        round_before_last_sales: int,
        identity_index: int,
    ) -> None:
        pass

    def policy(self, last_round_agents_prices: list[float]) -> float:
        return random.randint(0, 99)

    def learning_has_converged(self):
        return True

    def __str__(self):
        return "RandomAgent()"
