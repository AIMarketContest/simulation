from abc import ABCMeta, abstractmethod
from typing import List


class AgentNameMaker(metaclass=ABCMeta):
    """
    Creates and distributes agent names in a consistent way.
    """

    @abstractmethod
    def get_names(self) -> List[str]:
        """
        Returns the whole list of agent names.

        Returns
        _______
        List[str]
            List of agent names.

        Raises
        ______
        NotImplementedError
            If concrete class does not override method.
        """
        raise NotImplementedError

    @abstractmethod
    def get_name(self, index: int) -> str:
        """
        Returns the name of the agent with the given index.

        Parameters
        __________
        index : int
            The index of the agent whose name is to be returned.

        Returns
        _______
        str
            The name of the agent with the given index.

        Raises
        ______
        NotImplementedError
            If concrete class does not override method.
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, subclass: object) -> bool:
        return all(
            [
                hasattr(subclass, "get_names"),
                callable(getattr(subclass, "get_names")),
                hasattr(subclass, "get_name"),
                callable(getattr(subclass, "get_name")),
            ]
        )
