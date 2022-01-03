from ai_market_contest.agent import Agent
from ai_market_contest.typing.types import Price
from typing import List


class FixedAgentFifty(Agent):
    """
    An agent that always returns the same price of 50.
    """

    FIXED_PRICE: int = 50

    def update(self, last_round_profit: Price, identity_index: int) -> None:
        pass

    def get_initial_price(self) -> int:
        return self.FIXED_PRICE

    def get_price(self, last_round_agents_prices: List[Price], identity_index):
        return self.FIXED_PRICE
