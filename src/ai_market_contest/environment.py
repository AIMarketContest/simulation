from typing import Any, Dict, List, Optional

import numpy as np
from gym import spaces  # type: ignore
from numpy.typing import NDArray
from pettingzoo import ParallelEnv  # type: ignore
from pettingzoo.utils import from_parallel, wrappers  # type: ignore

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

    def __init__(self, simulation_length: int, demand: DemandFunction, max_agents: int):
        self.max_agents: int = max_agents
        self.possible_agents: List[str] = []
        self.agent_name_mapping: Dict[str, Agent] = {}
        self.action_spaces: Dict[
            Agent, spaces.Discrete
        ] = {}  # possible actions - from 0.000 in 0.001 increments
        self.observation_spaces: Dict[Agent, spaces.Discrete] = {}
        self.hist_set_prices: NDArray[np.float32] = np.zeros(
            (self.simulation_length, self.max_agents), dtype=np.float32
        )
        self.hist_sales_made: NDArray[np.int32] = np.zeros(
            (self.simulation_length, self.max_agents), dtype=np.int32
        )
        self.simulation_length: int = simulation_length
        self.demand: DemandFunction = demand
        self.agent_count: int = 0

    def reset(self) -> Dict[Agent, float]:
        self.possible_agents = []
        self.action_spaces = {}
        self.observation_spaces = {}
        self.hist_set_prices = np.zeros(
            (self.simulation_length, self.max_agents), dtype=np.float32
        )
        self.hist_sales_made = np.zeros(
            (self.simulation_length, self.max_agents), dtype=np.int32
        )
        self.time_step = 0

        return {agent: 0.0 for agent in self.possible_agents if agent is not None}

    def add_agent(self, agent: Agent) -> int:
        """
        Adds an agent to the simulation.
        Separated from constructor to allow mid-simulation entries

        Parameters
        ----------
        agent: Agent
            The agent to be added

        Returns
        -------
        int
            The id of the new agent added

        Raises
        ------
        IndexError
            If the simulation cannot handle any more agents.
        """
        if self.agent_count >= self.max_agents:
            raise RuntimeError("Cannot add more agents to simulation")

        self.possible_agents[self.agent_count] = f"agent_{self.agent_count}"
        self.action_spaces[agent] = spaces.Discrete(self.NUMBER_OF_DISCRETE_PRICES)
        self.observation_spaces[agent] = spaces.Discrete(self.NUMBER_OF_DISCRETE_PRICES)
        self.agent_count += 1

        return self.agent_count - 1

    def get_results(self) -> tuple[NDArray[np.float32], NDArray[np.int32]]:
        """
        Allows post-simulation analysis to be performed on sales figures and numbers

        Returns
        -------
        self.hist_set_prices: list[list[float]]
            The list represents the time slice of the simulation
            For a time slice we can use the inner list to find how many sales
            an agent made using their index in all_agents.
        self.hist_sales_made: list[list[int]]
            The list represents the time slice of the simulation
            For a time slice we can use the list to find what price an agent
            set using their index in all_agents.
        """
        return self.hist_set_prices, self.hist_sales_made

    def observe(self, agent: Agent) -> List[float]:
        agent_id = self.possible_agents.index(agent)
        return [
            self.hist_set_prices[x][agent_id] for x in range(len(self.hist_set_prices))
        ]

    def step(
        self, actions: Dict[Agent, float]
    ) -> tuple[
        Dict[Agent, float],
        Dict[Agent, float],
        Dict[Agent, bool],
        Dict[Agent, Any],
    ]:
        """
        Runs a time step for the simulation and appends results to the historic data
        """
        current_prices = [
            actions[agent] for agent in self.possible_agents if agent is not None
        ]
        demands = self.demand.get_sales(current_prices)
        self.hist_set_prices[self.time_step] = current_prices
        self.hist_sales_made[self.time_step] = demands

        self.time_step += 1
        if self.time_step >= self.simulation_length:
            # raise IndexError("Cannot run simulation beyond maximum time step")
            self.done = True

        observations: Dict[Agent, float] = {}
        rewards: Dict[Agent, float] = {}
        dones: Dict[Agent, bool] = {}
        infos: Dict[Agent, Any] = {}

        for index, agent in enumerate(self.possible_agents):
            if agent is not None:
                observations[agent] = demands[index]
                rewards[agent] = demands[index] * actions[agent]
                dones[agent] = self.done
                infos[agent] = {}

        return observations, rewards, dones, infos


def init_env(
    simulation_length: int, demand: DemandFunction, max_agents: int
) -> Environment:
    env = Environment(simulation_length, demand, max_agents)
    env = from_parallel(env)
    env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)

    return env
