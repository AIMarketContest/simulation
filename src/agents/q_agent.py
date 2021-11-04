from agent import Agent
from collections import defaultdict
import numpy as np


class QAgent(Agent):
    def __init__(self, action_spaces: int):
        self.cost = 0.3
        self.actions_spaces = action_spaces
        self.Q = defaultdict(lambda: np.zeros((action_spaces,)))
        self.alpha = 0.3
        self.gamma = 0.9

    def policy(self, last_round_agents_prices: list[float]) -> float:
        if tuple(last_round_agents_prices) in self.Q:
            return np.argmax(self.Q[tuple(last_round_agents_prices)])
        else:
            return np.random.randint(0, self.actions_spaces)

    ## TODO :: Change r1 to be sales figures (i.e. reward_signal = [price-cost]*r1)
    def update(
        self,
        s1: list[float],
        r1: int,
        s2: list[float],
        r2: int,
        identity_index: int,
    ) -> None:
        a1 = s1[identity_index]
        a2 = s2[identity_index]

        self.Q[tuple(s1)][a1] += self.alpha * (
            (r1 * a1)
            + self.gamma * np.argmax(self.Q[tuple(s2)])
            - self.Q[tuple(s1)][a1]
        )
