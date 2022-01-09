from collections import defaultdict
from typing import Dict, List, Sequence

import numpy as np

from ai_market_contest.agent import Agent
from ai_market_contest.typing.types import Price


class QAgent(Agent):
    def __init__(self, observation_space=None, action_space=None, config={}):
        super().__init__(observation_space, action_space, config)
        self.cost = 0.3
        self.actions_spaces = 100
        self.Q: Dict[Sequence[float], Dict[float, float]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.alpha = 0.3
        self.gamma = 0.9
        self.theta = 0.0005
        self.time = 0
        self.last_round_prices: List[Price] = []
        self.last_round_profit = 0

    def get_initial_price(self) -> Price:
        return 1

    def policy(self, last_round_agents_prices: List[Price], agent_index: int) -> float:
        self.last_round_prices = last_round_agents_prices
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

            price = int(best_price)

        else:
            price = np.random.randint(0, self.actions_spaces)

        return price

    def update(
        self,
        last_round_profit: int,
        identity_index: int,
    ) -> None:
        if not self.last_round_prices:
            return

        self.time += 1

        a1 = self.last_round_prices[identity_index]

        other_agent_prices = (
            self.last_round_prices[:identity_index]
            + self.last_round_prices[identity_index + 1 :]
        )

        max_path: float = np.argmax(self.Q[tuple(other_agent_prices)])  # type: ignore
        self.Q[tuple(other_agent_prices)][a1] += self.alpha * (
            last_round_profit
            + self.gamma * max_path
            - self.Q[tuple(other_agent_prices)][a1]
        )

    def probability_exploration(self):
        return (1 - self.theta) ** self.time

    def learning_has_converged(self):
        return True
