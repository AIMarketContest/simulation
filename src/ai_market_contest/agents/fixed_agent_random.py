from ai_market_contest.agent import Agent
import random


class FixedAgentRandom(Agent):
    """
    An agent that always returns the same price of 50.
    """

    FIXED_PRICE: int = random.randint(0, 99)

    def get_initial_price(self):
        return FIXED_PRICE

    def get_price(self, last_round_agents_prices: List[int], identity_index):
        return FIXED_PRICE
