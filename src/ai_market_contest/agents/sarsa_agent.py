from collections import defaultdict
from typing import Dict, Sequence, List

import numpy as np

from ai_market_contest.agent import Agent


class SarsaAgent(Agent):
    def __init__(self):
        self.cost = 0.3
        self.actions_spaces = 100
        self.Q: Dict[Sequence[float], Dict[float, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        self.alpha = 0.3
        self.gamma = 0.9
        self.theta = 0.001
        self.time = 0
        self.round_before_last_prices = []

    def policy(self, last_round_agents_prices: List[float], agent_index: int) -> float:
        self.round_before_last_prices = last_round_agents_prices
        other_agent_prices = (
            last_round_agents_prices[:agent_index]
            + last_round_agents_prices[agent_index + 1 :]
        )

        if (
            tuple(other_agent_prices) in self.Q
            and np.random.uniform(0, 1) > self.probability_exploration()
        ):
            previous_actions_for_state = self.Q[tuple(other_agent_prices)]

            max_profit = 0.0
            best_price = 0.0
            for price, profit in previous_actions_for_state.items():
                if profit > max_profit:
                    max_profit = profit
                    best_price = price

            return best_price

        return np.random.randint(0, self.actions_spaces)

    def update(
        self,
        last_round_profit: List[float],
        identity_index: int,
    ) -> None:
        self.time += 1

        a1 = last_round_prices[identity_index]
        a2 = self.round_before_last_prices[identity_index]

        last_round_prices = (
            last_round_prices[:identity_index] + last_round_prices[identity_index + 1 :]
        )
        round_before_last_prices = (
            self.round_before_last_prices[:identity_index]
            + self.round_before_last_prices[identity_index + 1 :]
        )

        self.Q[tuple(last_round_prices)][a1] += self.alpha * (
            (last_round_sales * a1)
            + self.gamma * self.Q[tuple(round_before_last_prices)][a2]
            - self.Q[tuple(last_round_prices)][a1]
        )

    def probability_exploration(self):
        return (1 - self.theta) ** self.time

    def learning_has_converged(self):
        return True
