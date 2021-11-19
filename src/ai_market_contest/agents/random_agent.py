import random

from ai_market_contest.agent import Agent


class RandomAgent(Agent):
    """
    An agent which returns a random price.
    """

    def update(
        self,
        s1: list[float],
        r1: int,
        s2: list[float],
        r2: int,
        identity_index: int,
    ) -> None:
        pass

    def policy(self, last_round_agents_prices: list[float], agent_index: int) -> float:
        return random.random()
