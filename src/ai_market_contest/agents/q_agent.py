from collections import defaultdict
from typing import Dict, Sequence, List

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

    def policy(self, last_round_agents_prices: List[float], agent_index: int) -> float:
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
        last_round_prices: List[float],
        last_round_sales: int,
        round_before_last_prices: List[float],
        round_before_last_sales: int,
        identity_index: int,
    ) -> None:
        self.time += 1

        a1 = last_round_prices[identity_index]

        last_round_prices = (
            last_round_prices[:identity_index] + last_round_prices[identity_index + 1 :]
        )
        round_before_last_prices = (
            round_before_last_prices[:identity_index]
            + round_before_last_prices[identity_index + 1 :]
        )

        max_path: float = np.argmax(
            self.Q[tuple(round_before_last_prices)]
        )  # type: ignore
        self.Q[tuple(last_round_prices)][a1] += self.alpha * (
            (last_round_sales * a1)
            + self.gamma * max_path
            - self.Q[tuple(last_round_prices)][a1]
        )

    def probability_exploration(self):
        return (1 - self.theta) ** self.time

    def learning_has_converged(self):
        return True
