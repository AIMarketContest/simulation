from ai_market_contest.agent import Agent
from ai_market_contest.typing.types import Price
from typing import List
import random


class FixedAgentRandom(Agent):
    """
    An agent that always returns the same price of 50.
    """

    FIXED_PRICE: int = random.randint(0, 99)

    def update(self, last_round_profit: Price, identity_index: int) -> None:
        pass

    def get_initial_price(self) -> Price:
        return self.FIXED_PRICE

    def get_price(self, last_round_agents_prices: List[Price], identity_index) -> Price:
        return self.FIXED_PRICE
