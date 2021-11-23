from typing import Any, Dict, List

from gym import spaces  # type: ignore
from pettingzoo import ParallelEnv  # type: ignore
from pettingzoo.utils import from_parallel, wrappers  # type: ignore
import functools
from gym.spaces import Discrete, Tuple

from ai_market_contest.agent import Agent
from ai_market_contest.demand_function import DemandFunction


class Environment(ParallelEnv):
    """
    The backbone of the simulation - responsible for tying most other elements together

    Attributes
    ----------
    all_agents: list[Agent]
        Represents a list of all agents partaking in the simulation
    hist_sales_made: list[list[int]]
        The list represents the time slice of the simulation
        For a time slice we can use the inner list to find how many sales an
        agent made using their index in all_agents.
    hist_set_prices: list[list[float]]
        The list represents the time slice of the simulation
        For a time slice we can use the list to find what price an agent set
        using their index in all_agents.
        (These are separate attributes since we need to be able to give an agent
        hist_set_prices without letting them see hist_sales_made)
    simulation_length: int
        Used to keep track of when the simulation is "complete". Must be positive
    time_step: int
        Used to keep track of the simulation time elapsed. Must be positive
    demand: DemandFunction
        Reposible for generating a demand function (interchangeable)
    max_agents: int
        Represents the maximum number of agents the simulation can support
    agent_count: int
        The number of agents currently in the simulation
    """

    START_VAL = 0.5
    NUMBER_OF_DISCRETE_PRICES = 100

    metadata = {"render.modes": ["human"], "name": "rps_v2"}

    def __init__(
        self,
        agents: List[Agent],
        simulation_length: int,
        demand: DemandFunction,
    ):
        self.possible_agents: List[str] = [
            "player_" + str(r) for r in range(len(agents))
        ]
        self.agents = self.possible_agents[:]
        self.agent_name_mapping: dict[str, Agent] = {
            agent_name: agent for agent_name, agent in zip(self.possible_agents, agents)
        }
        self.simulation_length: int = simulation_length
        self.demand: DemandFunction = demand
        self.time_step: int = 0
        self.reset()

    def reset(self) -> Dict[str, float]:
        return {agent: 0.0 for agent in self.possible_agents if agent is not None}

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent: str):
        return Tuple([Discrete(self.NUMBER_OF_DISCRETE_PRICES)] * len(self.agents))

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent: str):
        return Tuple([Discrete(self.NUMBER_OF_DISCRETE_PRICES)] * len(self.agents))

    def step(
        self, actions: Dict[str, int]
    ) -> tuple[Dict[str, float], Dict[str, float], Dict[str, bool], Dict[str, Any],]:
        """
        Runs a time step for the simulation and appends results to the historic data
        """
        demands = self.demand.get_sales(actions)
        self.time_step += 1
        if self.time_step >= self.simulation_length:
            # raise IndexError("Cannot run simulation beyond maximum time step")
            self.done = True

        observations: Dict[str, float] = {}
        rewards: Dict[str, float] = {}
        dones: Dict[str, bool] = {}
        infos: Dict[str, Any] = {}

        for agent in self.possible_agents:
            observations[agent] = demands[agent]
            rewards[agent] = demands[agent] * actions[agent]
            dones[agent] = self.done
            infos[agent] = {}

        return observations, rewards, dones, infos


def init_env(
    agents: List[Agent], simulation_length: int, demand: DemandFunction
) -> Environment:
    env = Environment(agents, simulation_length, demand)
    env = from_parallel(env)
    env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)

    return env
