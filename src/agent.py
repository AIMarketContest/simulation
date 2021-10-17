from abc import ABCMeta, abstractmethod


class Agent(metaclass=ABCMeta):
    """
    Agent interface - an agent represents a firm selling a product in the market.

    An agent encapsulates the users private pricing strategy.
    The agent must give an initial price for the product
    and given its sales for the last round
    and all prices set by competitors in that round
    it must give its new price.

    Methods
    -------
    get_initial_price()
        Represents the initial price of the product set by the agent (at timestep = 0).
    get_price(last_round_all_agents_prices, last_round_sales)
        Calculate the agent's price at the current timestep using data from the previous timestep.
    """

    @abstractmethod
    def get_initial_price(self):
        raise NotImplementedError

    @abstractmethod
    def get_price(self, last_round_all_agents_prices, last_round_sales):
        raise NotImplementedError
