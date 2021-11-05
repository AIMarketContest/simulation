import random

from agent import Agent


class RandomAgent(Agent):
    """
    An agent which returns a random price.
    """

    def update(
        self,
        last_round_agents_prices: list[float],
        last_round_sales: int,
        identity_index: int,
    ) -> None:
        pass

    def policy(self) -> float:
        return random.random()
