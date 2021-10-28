from abc import ABCMeta, abstractmethod


class Agent(metaclass=ABCMeta):
    """
    Agent interface - an agent represents a firm selling a product in the market.

    An agent encapsulates the users private pricing strategy.
    The agent must give an initial price for the product
    and given its sales for the last round
    and all prices set by competitors in that round
    it must give its new price.
    """

    @abstractmethod
    def get_initial_price(self) -> float:
        """
        Represents the initial price of the product set by the agent (at timestep = 0).

        Returns
        -------
        float
            Price of the product set by the agent at timestep = 0, discretised within [0,1].

        Raises
        ______
        NotImplementedError
            If concrete class does not override method.
        """

        raise NotImplementedError

    @abstractmethod
    def get_price(
        self,
        last_round_agents_prices: list[float],
        last_round_sales: int,
        identity_index: int,
    ) -> float:
        """
        Calculate the agent's price at the current timestep using data from the previous timestep.

        Parameters
        __________
        last_round_all_agents_prices : list of float
            List of all the prices set by all agents in the previous timestep.
        last_round_sales: int
            A positive integer representing the number of sales the agent made in the previous timestep.
        identity_index: int
            A positive integer that tells the agent which index in the list
            corresponds to themself.

        Returns
        -------
        float
            Price of the product set by the agent at the current timestep, discretised within [0,1].

        Raises
        ______
        NotImplementedError
            If concrete class does not override method.
        """

        raise NotImplementedError

    def learning_has_converged(self):
        """
        Check if the agent's learning has converged.

        Returns
        -------
        bool : True if the agent learning has converged, False otherwise.
        """
        return False


    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            all(
                [
                    hasattr(subclass, "get_initial_price"),
                    callable(subclass.get_initial_price),
                    hasattr(subclass, "get_price"),
                    callable(subclass.get_price),
                ]
            )
            or NotImplemented
        )
