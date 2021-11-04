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
    def policy(self, last_round_agents_prices: list[float]) -> float:
        """
        Query the agent for the next price to set.

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

    @abstractmethod
    def update(
        self,
        s1: list[float],
        r1: int,
        s2: list[float],
        r2: int,
        identity_index: int,
    ) -> None:
        """
        Feeds data from the previous timestep into the agent allowing it to adjust it's strategy.

        Parameters
        __________
        last_round_all_agents_prices : list of float
            List of all the prices set by all agents in the previous timestep.
        last_round_sales: int
            A positive integer representing the number of sales the agent made in the previous timestep.
        identity_index: int
            A positive integer that tells the agent which index in the list
            corresponds to themself.

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
                    hasattr(subclass, "policy"),
                    callable(subclass.policy),
                    hasattr(subclass, "update"),
                    callable(subclass.update),
                ]
            )
            or NotImplemented
        )
