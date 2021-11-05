from agent import Agent
from collections import defaultdict
import numpy as np


class SarsaAgent(Agent):
    def __init__(self, action_spaces: int):
        self.cost = 0.3
        self.actions_spaces = action_spaces
        self.Q = defaultdict(lambda: defaultdict(int))
        self.alpha = 0.3
        self.gamma = 0.9
        self.theta = 0.001
        self.time = 0

    def policy(self, last_round_agents_prices: list[float], agent_index: int) -> float:
        other_agent_prices = (
            last_round_agents_prices[:agent_index]
            + last_round_agents_prices[agent_index + 1 :]
        )

        if (
            tuple(other_agent_prices) in self.Q
            and np.random.uniform(0, 1) > self.probability_exploration()
        ):
            previous_actions_for_state = self.Q[tuple(other_agent_prices)]

            max_profit = 0
            best_price = 0
            for price, profit in previous_actions_for_state.items():
                if profit > max_profit:
                    max_profit = profit
                    best_price = price

            return best_price

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
        self.time += 1

        a1 = s1[identity_index]
        a2 = s2[identity_index]

        s1 = s1[:identity_index] + s1[identity_index + 1 :]
        s2 = s2[:identity_index] + s2[identity_index + 1 :]

        self.Q[tuple(s1)][a1] += self.alpha * (
            (r1 * a1) + self.gamma * self.Q[tuple(s2)][a2] - self.Q[tuple(s1)][a1]
        )

    def probability_exploration(self):
        return (1 - self.theta) ** self.time
