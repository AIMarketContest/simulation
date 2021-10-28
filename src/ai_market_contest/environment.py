import numpy as np
from numpy.typing import NDArray

from typing import Dict, List
from gym import spaces
from agent import Agent
from demand_function import DemandFunction
from pettingzoo import AECEnv

from pettingzoo.utils import wrappers


def env(simulation_length: int, demand: DemandFunction):
    """
    The env function wraps the environment in 3 wrappers by default. These
    wrappers contain logic that is common to many pettingzoo environments.
    We recommend you use at least the OrderEnforcingWrapper on your own environment
    to provide sane error messages. You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    env = Environment(simulation_length, demand)
    env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)

    return env


class Environment(AECEnv):
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

    def __init__(self, simulation_length: int, demand: DemandFunction):
        self.possible_agents: NDArray = np.empty((max_agents,), dtype=object)
        self.action_spaces: Dict[Agent, spaces.Discrete] = {}
        self.observation_spaces: Dict[Agent, spaces.Discrete] = {}
        self.hist_sales_made: NDArray = np.zeros(
            (simulation_length, max_agents), dtype=int
        )
        self.hist_set_prices: NDArray = np.zeros(
            (simulation_length, max_agents), dtype=float
        )
        self.simulation_length: int = simulation_length
        self.time_step: int = 0
        self.demand: DemandFunction = demand
        self.agent_count: int = 0
        self.max_agents: int = max_agents

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

        self.all_agents[self.agent_count] = agent
        self.action_spaces[agent] = spaces.Discrete(100)
        self.observation_spaces[agent] = spaces.Discrete(100)
        self.agent_count += 1

        return self.agent_count - 1

    def get_results(self) -> tuple[NDArray, NDArray]:
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

    def reset(self):
        self.possible_agents = []
        self.action_spaces = {}
        self.observation_spaces = {}
        self.hist_sales_made = []
        self.hist_set_prices = []
        self.time_step = 0

    def step(self) -> None:
        """
        Runs a time step for the simulation and appends results to the historic data
        """

        if self.time_step >= self.simulation_length:
            raise IndexError("Cannot run simulation beyond maximum time step")

        current_prices: list[float] = [0.0] * self.agent_count
        if self.time_step == 0:
            for agent_index, agent in enumerate(self.possible_agents):
                current_prices[agent_index] = agent.get_initial_price()
        else:
            prior_sales: list[int] = self.hist_sales_made[self.time_step - 1]

            for agent_index, agent in enumerate(self.possible_agents):
                prior_sales_for_agent: int = prior_sales[agent_index]
                current_prices[agent_index] = agent.get_price(
                    self.hist_set_prices[self.time_step - 1],
                    prior_sales_for_agent,
                    agent_index,
                )

        self.hist_set_prices[self.time_step] = current_prices
        self.hist_sales_made[self.time_step] = np.array(
            self.demand.get_sales(current_prices)
        )
        self.time_step += 1
