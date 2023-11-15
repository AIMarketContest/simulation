import math  # type: ignore

from gym.spaces.discrete import Discrete  # type: ignore
from gym.spaces.multi_discrete import MultiDiscrete  # type: ignore
from ray.rllib.env.multi_agent_env import MultiAgentEnv  # type: ignore
from ray.rllib.utils.typing import MultiAgentDict  # type: ignore

from ai_market_contest.demand_function import DemandFunction  # type: ignore
from ai_market_contest.training.agent_name_maker import AgentNameMaker  # type: ignore
from ai_market_contest.typing.types import Price  # type: ignore


class Market(MultiAgentEnv):
    START_VAL = 50
    NUMBER_OF_DISCRETE_PRICES = 100
    MAX_SALES = 100

    def __init__(
        self,
        demand_function: DemandFunction,
        simulation_length: int,
        agent_name_maker: AgentNameMaker,
    ):
        self.agents: list[str] = agent_name_maker.get_names()

        self.observation_space = MultiDiscrete(
            [self.NUMBER_OF_DISCRETE_PRICES for _ in range(len(self.agents))]
        )
        self.action_space = Discrete(self.NUMBER_OF_DISCRETE_PRICES)

        self.reward_range = (-math.inf, math.inf)
        self.demand = demand_function
        self.done = False
        self.simulation_length = simulation_length
        self.time_step = 0

        self.agent_name_maker = agent_name_maker

    def reset(self):
        self.time_step = 0
        self.done = False
        return {agent: [self.START_VAL for _ in self.agents] for agent in self.agents}

    def step(
        self, action_dict: MultiAgentDict
    ) -> tuple[MultiAgentDict, MultiAgentDict, MultiAgentDict, MultiAgentDict]:
        demands = self.demand.get_sales(action_dict)
        self.time_step += 1
        if self.time_step >= self.simulation_length:
            self.done = True
        last_round_all_agents_prices: list[Price] = [
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
