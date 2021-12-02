import pathlib
from abc import ABCMeta, abstractmethod

from ai_market_contest.agent import Agent  # type: ignore
from ai_market_contest.environment import Environment  # type: ignore


class TrainConfig(metaclass=ABCMeta):
    """
    Interface for configuring a training session.
    """

    @abstractmethod
    def create_environment(self, agent_to_train: Agent) -> Environment:
        """
        Returns an environment set up for the training regimine.

        Parameters
        ----------
        agent_to_train : Agent
            The agent the training configuration is designed to train.

        Returns
        ----------
        Environment
            An Environment set up with the rules outlined by the configuration.

        Raises
        ------
        NotImplementedError
            If concrete class does not override method.
        """

        raise NotImplementedError

    @abstractmethod
    def write_config_to_file(self, path: pathlib.Path):
        """
        Saves the configuration class as a configuration file.

        Parameters
        ----------
        path : pathlib.Path
            Where the configuration file should be written to.
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            all(
                [
                    hasattr(subclass, "set_up_environment"),
                    callable(subclass.set_up_environment),
                    hasattr(subclass, "write_config_to_file"),
                    callable(subclass.write_config_to_file),
                ]
            )
            or NotImplemented
        )
