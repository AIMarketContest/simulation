import random
from typing import List

from ai_market_contest.agent import Agent
from ai_market_contest.typing.types import Price  # type: ignore


class RandomAgent(Agent):
    """
    An agent which returns a random price.
    """

    def update(self, last_round_profit: Price, identity_index: int) -> None:
        pass

    def get_initial_price(self) -> Price:
        return random.randint(0, 99)

    def policy(self, last_round_agents_prices: List[Price], identity_index) -> Price:
        return random.randint(0, 99)
