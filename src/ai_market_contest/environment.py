import math
from typing import List, Tuple

from gym.spaces.discrete import Discrete  # type: ignore
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from ray.rllib.utils.typing import MultiAgentDict

from ai_market_contest.demand_function import DemandFunction


class Market(MultiAgentEnv):
    START_VAL = 50
    NUMBER_OF_DISCRETE_PRICES = 100
    MAX_SALES = 100

    def __init__(
        self, num_agents: int, demand_function: DemandFunction, simulation_length: int
    ):
        self.agents: List[str] = ["player_" + str(r) for r in range(num_agents)]

        self.observation_space = MultiDiscrete(
            [self.NUMBER_OF_DISCRETE_PRICES] * num_agents
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
        return {agent: 0 for agent in self.agents}

    def step(
        self, action_dict: MultiAgentDict
    ) -> Tuple[MultiAgentDict, MultiAgentDict, MultiAgentDict, MultiAgentDict]:
        demands = self.demand.get_sales(action_dict)
        self.time_step += 1
        if self.time_step >= self.simulation_length:
            # raise IndexError("Cannot run simulation beyond maximum time step")
            self.done = True
        last_round_all_agents_prices: List[float] = [
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
