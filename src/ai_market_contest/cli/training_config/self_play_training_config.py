import configparser
import copy
import pathlib

from ai_market_contest.agent import Agent  # type: ignore
from ai_market_contest.cli.cli_config import TRAIN_CONFIG_FILENAME  # type: ignore
from ai_market_contest.cli.training_config.train_config import (
    TrainConfig,  # type: ignore
)
from ai_market_contest.demand_function import DemandFunction  # type: ignore
from ai_market_contest.demandfunctions.gaussian_demand_function import (
    GaussianDemandFunction,  # type: ignore
)
from ai_market_contest.environment import Environment  # type: ignore


class SelfPlayTrainingConfig(TrainConfig):
    """
    Configuration class for agents to train via self-play.

    Attributes
    ----------
    number_of_agents: int
        The number of agents to play in the self-play game.
    training_duration: int
        The duration for the simulation.
    demand_function: DemandFunction
        The demand function to be used by the environment during the simulation.
    """

    def __init__(
        self,
        number_of_agents: int = 5,
        training_duration: int = 100,
        demand_function: DemandFunction = GaussianDemandFunction(),
    ):
        """
        Parameters
        ----------
        number_of_agents: int, default=5
            The number of agents to play in the self-play game.
        training_duration: int, default=100
            The duration for the simulation.
        demand_function: DemandFunction, default=GaussianDemandFunction()
            The demand function to be used by the environment during the simulation.
        """
        self.number_of_agents: int = number_of_agents
        self.training_duration: int = training_duration
        self.demand_function: DemandFunction = demand_function

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
        """
        env: Environment = Environment(
            self.training_duration, self.demand_function, self.number_of_agents
        )  # max_agents has +1 to make room for the agent to be trained
        env.add_agent(agent_to_train)
        for _ in range(
            1, self.number_of_agents
        ):  # start from 1 as the first agent to train has been added
            env.add_agent(copy.deepcopy(agent_to_train))

        return env

    def write_config_to_file(self, path: pathlib.Path):
        """
        Saves the configuration class as a configuration file.

        Parameters
        ----------
        path : pathlib.Path
            Where the configuration file should be written to.
        """
        config: configparser.ConfigParser = configparser.ConfigParser()
        config["training"] = {
            "type": "self-play",
            "number of agents": int(self.number_of_agents),
        }
        config["environment"] = {
            "demand function": str(self.demand_function),
            "training duration": str(self.training_duration),
        }

        with open(path / TRAIN_CONFIG_FILENAME, "w") as f:
            config.write(f)

    def set_number_of_agents(self, number_of_agents: int):
        """
        Allows the user to change the number of agents to play in self-play.

        Parameters
        ----------
        number_of_agents : int
            The number of agents to play in self-play.
        """
        self.number_of_agents = number_of_agents

    def set_training_duration(self, training_duration: int):
        """
        Allows the user to change the number of time steps before the
        training simulation ends.

        Parameters
        ----------
        training_duration : int
            The new duration for the simulation.
        """
        self.training_duration = training_duration

    def set_demand_function(self, demand_function: DemandFunction):
        """
        Allows the user to change the demand function used by the
        environment in the training.

        Parameters
        ----------
        demand_function : DemandFunction
            The new demand function to be used.
        """
        self.demand_function = demand_function
