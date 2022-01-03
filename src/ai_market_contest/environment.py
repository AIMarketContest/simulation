import math # type: ignore
from typing import List, Tuple # type: ignore

from gym.spaces.discrete import Discrete # type: ignore
from gym.spaces.multi_discrete import MultiDiscrete  # type: ignore
from ray.rllib.env.multi_agent_env import MultiAgentEnv # type: ignore
from ray.rllib.utils.typing import MultiAgentDict # type: ignore

from ai_market_contest.demand_function import DemandFunction # type: ignore
from ai_market_contest.typing.types import Price # type: ignore


class Market(MultiAgentEnv):
    START_VAL = 50
    NUMBER_OF_DISCRETE_PRICES = 100
    MAX_SALES = 100

    def __init__(
        self, num_agents: int, demand_function: DemandFunction, simulation_length: int
    ):
        self.agents: List[str] = ["player_" + str(r) for r in range(num_agents)]

        self.observation_space = MultiDiscrete(
            [self.NUMBER_OF_DISCRETE_PRICES for _ in range(num_agents)]
        )
        self.action_space = Discrete(self.NUMBER_OF_DISCRETE_PRICES)

        self.reward_range = (-math.inf, math.inf)
        self.demand = demand_function
        self.done = False
        self.simulation_length = simulation_length
        self.time_step = 0

    def reset(self):
        self.time_step = 0
        self.done = False
        return {agent: [self.START_VAL for _ in self.agents] for agent in self.agents}

    def step(
        self, action_dict: MultiAgentDict
    ) -> Tuple[MultiAgentDict, MultiAgentDict, MultiAgentDict, MultiAgentDict]:
        demands = self.demand.get_sales(action_dict)
        self.time_step += 1
        if self.time_step >= self.simulation_length:
            self.done = True
        last_round_all_agents_prices: List[Price] = [
            price for _, price in action_dict.items()
        ]
        observations: MultiAgentDict = {}
        rewards: MultiAgentDict = {}
        dones: MultiAgentDict = {}
        infos: MultiAgentDict = {}

        for agent_index, agent in enumerate(self.agents):
            observations[agent] = last_round_all_agents_prices
            rewards[agent] = demands[agent] * action_dict[agent]
            dones["__all__"] = self.done
            infos[agent] = {"identity_index": agent_index}
        return observations, rewards, dones, infos
