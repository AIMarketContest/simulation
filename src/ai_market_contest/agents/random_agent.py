import random
from ai_market_contest.agent import Agent
from ai_market_contest.typing.types import Price
from typing import List


class RandomAgent(Agent):
    """
    An agent which returns a random price.
    """

    def update(self, last_round_profit: Price, identity_index: int) -> None:
        pass

    def get_initial_price(self) -> Price:
        return random.randint(0, 99)

    def get_price(self, last_round_agents_prices: List[Price], identity_index) -> Price:
        return random.randint(0, 99)

    def __str__(self):
        return "RandomAgent()"
