from abc import ABCMeta, abstractmethod


class DemandFunction(metaclass=ABCMeta):
    """
    The demand function is a map of the price of a product to its sales.

    The demand function must give the quantity of the product
    that will be sold by any agent in the market at a given price.
    """

    @abstractmethod
    def get_sales(self, current_prices: list[float]) -> list[int]:
        """
        Calculates the quantity of the product that will be sold at a given
        price.

        Parameters
        __________
        current_prices : list[float]
            The current price of the product set by all agents.

        Returns
        _______
        list[int]
            The quantity of item sold by each agent, indexed by where their
            price appeared in `round_prices`.

        Raises
        ______
        NotImplementedError
            If concrete class does not override method.
        """

        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            all(
                [
                    hasattr(subclass, "get_sales"),
                    callable(getattr(subclass, "get_sales")),
                ]
            )
            or NotImplemented
        )
