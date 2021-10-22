import random

from agent import Agent


class RandomAgent(Agent):
    """
    An agent which returns a random price.
    """

    def get_initial_price(self) -> float:
        return random.random()

    def get_price(
        self,
        last_round_agents_prices: list[float],
        last_round_sales: int,
        identity_index: int,
    ) -> float:
        return random.random()
