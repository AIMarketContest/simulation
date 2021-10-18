from src.agent import Agent
from src.demandfunction import DemandFunction


class Environment:
    """
    The backbone of the simulation - responsible for tying most other elements together

    Attributes
    ----------
    all_agents: list[Agent]
        Represents a list of all agents partaking in the simulation
    hist_sales_made: list[dict[Agent, int]]
        The list represents the time slice of the simulation
        For a time slice we can use the dict to find how many sales an agent made
    hist_set_prices: list[dict[Agent, float]]
        The list represents the time slice of the simulation
        For a time slice we can use the dict to find what price an agent set
            (These are separate attributes since we need to be able to give an agent ...
            ... hist_set_prices without letting them see hist_sales_made)
    simulation_length: int
        Used to keep track of when the simulation is "complete"
    time_step: int
        Used to keep track of the simulation time elapsed
    demand: DemandFunction
        Holds the class responsible for generating a demand function (interchangeable)
    """

    def __init__(self, simulation_length: int, demand: DemandFunction):
        self.all_agents: list[Agent] = []
        self.hist_sales_made: list[dict[Agent, int]] = [{}]
        self.hist_set_prices: list[dict[Agent, float]] = [{}]
        self.simulation_length: int = simulation_length
        self.time_step: int = 0
        self.demand: DemandFunction = demand

    def add_agent(self, agent: Agent) -> None:
        """
        Adds an agent to the simulation.
        Separated from constructor to allow mid-simulation entries

        Parameters
        ----------
        agent: Agent
            The agent to be added
        """
        self.all_agents.append(agent)
        index = max(self.time_step - 1, 0)
        self.hist_sales_made[index][agent] = 0

    def get_results(self) -> tuple[list[dict[Agent, float]], list[dict[Agent, int]]]:
        """
        Allows post-simulation analysis to be performed on sales figures and numbers

        Returns
        -------
        self.hist_set_prices: list[dict[Agent, float]]
            The list represents the time slice of the simulation
            For a time slice we can use the dict to find how many sales an agent made
        self.hist_sales_made: list[dict[Agent, int]]
            The list represents the time slice of the simulation
            For a time slice we can use the dict to find what price an agent set
        """
        return self.hist_set_prices, self.hist_sales_made

    def run_next_time_step(self) -> None:
        """
        Runs a time step for the simulation and appends results to the historic data
        """
        if ++self.time_step >= self.simulation_length:
            raise IndexError('Cannot run simulation beyond maximum time step')

        current_prices: dict[Agent, int] = {}

        prior_sales: dict[Agent, int] = self.hist_sales_made[-1]

        for agent in self.all_agents:
            prior_sales_for_agent: int = prior_sales[agent]
            current_prices[agent]: dict[Agent, float] = agent.get_price(self.hist_set_prices, prior_sales_for_agent)

        self.hist_set_prices.append(current_prices)
        self.hist_sales_made.append(self.demand.get_sales(current_prices))
