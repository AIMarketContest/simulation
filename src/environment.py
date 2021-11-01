from abc import ABC
from typing import Dict, List
from gym import spaces
from src.agent import Agent
from src.demand_function import DemandFunction
from pettingzoo import AECEnv
import numpy as np
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
    """
    START_VAL = 0.5

    def __init__(self, simulation_length: int, demand: DemandFunction):
        self.possible_agents: List[Agent] = []
        self.action_space: spaces.Discrete = spaces.Discrete(1000)  # possible actions - from 0.000 in 0.001 increments
        self.observation_spaces: spaces.MultiDiscrete = spaces.MultiDiscrete([self.START_VAL] * len(
            self.possible_agents))
        self.hist_sales_made: list[list[int]] = []
        self.hist_set_prices: list[list[float]] = []
        self.simulation_length: int = simulation_length
        self.time_step: int = 0
        self.demand: DemandFunction = demand
        self.done: bool = False
        self.state = 0

    def add_agent(self, agent: Agent) -> None:
        """
        Adds an agent to the simulation.
        Separated from constructor to allow mid-simulation entries

        Parameters
        ----------
        agent: Agent
            The agent to be added
        """
        self.possible_agents.append(agent)
        self.action_space = spaces.Discrete(1000)
        self.observation_spaces = spaces.Discrete(1000)

    def get_results(self) -> tuple[list[list[float]], list[list[int]]]:
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

    def reset(self) -> int:
        self.possible_agents = []
        self.action_spaces = {}
        self.observation_spaces = {}
        self.hist_sales_made = []
        self.hist_set_prices = []
        self.time_step = 0
        self.hist_set_prices = []
        self.state = np.random.randint(0, 1000, size=1)

        return self.state

    def step(self, actions) -> tuple[list[float], list[int], bool]:
        """
        Runs a time step for the simulation and appends results to the historic data
        """
        if self.time_step >= self.simulation_length:
            # raise IndexError("Cannot run simulation beyond maximum time step")
            self.done = True

        # Run current time step
        current_prices: list[float] = []
        for agent in self.possible_agents:
            current_prices.append(agent.policy())

        self.hist_set_prices.append(current_prices)
        self.hist_sales_made.append(self.demand.get_sales(current_prices))

        # Provide agent feedback on step
        sales: list[int] = self.hist_sales_made[-1]
        for agent_index, agent in enumerate(self.possible_agents):
            agent.update(
                self.hist_set_prices[-1], sales[agent_index], agent_index
            )

        self.time_step += 1
        demands = self.demand.get_sales(current_prices)
        rewards = [a * b for a, b in zip(demands, current_prices)]
        return current_prices, demands, self.done
