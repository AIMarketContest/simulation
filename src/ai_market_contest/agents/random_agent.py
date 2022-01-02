import random

from ai_market_contest.agent import Agent


class RandomAgent(Agent):
    """
    An agent which returns a random price.
    """

    def get_initial_price(self):
        return random.randint(0, 99)

    def get_price(self, last_round_agents_prices: List[int], identity_index):
        return random.randint(0, 99)

    def __str__(self):
        return "RandomAgent()"
