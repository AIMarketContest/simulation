import numpy as np
from numpy.typing import NDArray

from agent import Agent
from demand_function import DemandFunction


class Environment:
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

    def __init__(self, simulation_length: int, demand: DemandFunction, max_agents: int):
        self.all_agents: NDArray = np.empty((max_agents,), dtype=object)
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
            raise IndexError("Cannot add more agents to simulation")

        self.all_agents[self.agent_count] = agent
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

    def run_next_time_step(self) -> None:
        """
        Runs a time step for the simulation and appends results to the historic data
        """

        if self.time_step >= self.simulation_length:
            raise IndexError("Cannot run simulation beyond maximum time step")

        current_prices: list[float] = [0.0] * self.agent_count
        if self.time_step == 0:
            for agent_index, agent in enumerate(self.all_agents):
                current_prices[agent_index] = agent.get_initial_price()
        else:
            prior_sales: list[int] = self.hist_sales_made[self.time_step - 1]

            for agent_index, agent in enumerate(self.all_agents):
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
