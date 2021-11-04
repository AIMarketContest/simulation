from agent import Agent
from environment import Environment
from collections import defaultdict

from numpy import np


class QAgent(Agent):
    def __init__(self, env: Environment):
        self.curr_price = 0
        self.env = env
        self.cost = 0.3
        self.env.add_agent(self)
        self.Q = defaultdict(lambda: np.zeros(self.env.action_space.n))
        self.alpha = 0.1
        self.gamma = 0.9

    def policy(self, last_round_agents_prices: list[float]) -> float:
        if self.Q[last_round_agents_prices]:
            return np.argmax(self.Q[last_round_agents_prices])
        else:
            return np.random.randint(0, self.env.action_space.n)

    def get_reward(self, demand: float) -> float:
        pass

    def update(
        self,
        s1: list[float],
        a1: int,
        r1: int,
        s2: list[float],
        a2: int,
        r2: int,
        identity_index: int,
    ) -> None:
        self.Q[s1][a1] = self.Q[s1][a1] + self.alpha * (
            r1 + self.gamma * self.Q[s2][np.argmax(self.Q[s2])] - self.Q[s1][a1]
        )
