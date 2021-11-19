from collections import defaultdict
from typing import (
    Dict,
    Sequence,
)

import numpy as np

from ai_market_contest.agent import Agent


class QAgent(Agent):
    def __init__(self, action_spaces: int):
        self.cost = 0.3
        self.actions_spaces = action_spaces
        self.Q: Dict[Sequence[float], Dict[float, float]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.alpha = 0.3
        self.gamma = 0.9
        self.theta = 0.0005
        self.time = 0

    def policy(
        self, last_round_agents_prices: list[float], agent_index: int
    ) -> float:
        other_agent_prices = (
            last_round_agents_prices[:agent_index]
            + last_round_agents_prices[agent_index + 1 :]
        )

        if (
            tuple(other_agent_prices) in self.Q
            and np.random.uniform(0, 1) > self.probability_exploration()
        ):
            previous_actions_for_state = self.Q[tuple(other_agent_prices)]

            max_profit: float = 0.0
            best_price: float = 0.0
            for price, profit in previous_actions_for_state.items():
                if profit > max_profit:
                    max_profit = profit
                    best_price = price

            return best_price

        return np.random.randint(0, self.actions_spaces)

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

        s1 = s1[:identity_index] + s1[identity_index + 1 :]
        s2 = s2[:identity_index] + s2[identity_index + 1 :]

        max_path: float = np.argmax(self.Q[tuple(s2)])  # type: ignore
        self.Q[tuple(s1)][a1] += self.alpha * (
            (r1 * a1) + self.gamma * max_path - self.Q[tuple(s1)][a1]
        )

    def probability_exploration(self):
        return (1 - self.theta) ** self.time
