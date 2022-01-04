from ai_market_contest.agent import Agent
from ai_market_contest.typing.types import Price
from typing import List
import random


class TestAgent(Agent):
    """
    Agent interface - an agent represents a firm selling a product in the market.

    An agent encapsulates the users private pricing strategy.

    The user is free to implement this interface in order to test strategies.
    As is standard for ML models, it uses the policy-update format.
    For those not familiar with policy-update, see the comments on each function.
    """

    def __init__(self, observation_space=None, action_space=None, config={}):
        super().__init__(observation_space, action_space, config)
        self.lowest_price = False

    def get_initial_price(self) -> Price:
        """
        Query the agent for the initial price to set.

        Returns
        -------
        float
            Price of the product set by the agent at the current timestep,
            discretised within [0,100].

        Raises
        ------
        NotImplementedError
            If concrete class does not override method.
        """
        return 0

    def policy(
        self, last_round_all_agents_prices: List[Price], identity_index: int
    ) -> Price:
        """
        Query the agent for the next price to set.

        Parameters
        ----------
        last_round_all_agents_prices : list of float
            List of all the prices set by all agents in the previous timestep.
        identity_index: int
            A positive integer that tells the agent which index in the list
            corresponds to themself.

        Returns
        -------
        float
            Price of the product set by the agent at the current timestep,
            discretised within [0,100].

        Raises
        ------
        NotImplementedError
            If concrete class does not override method.
        """
        if self.lowest_price:
            return min(last_round_all_agents_prices)
        else:
            return random.choice(last_round_all_agents_prices)

    def update(self, last_round_profit: Price, identity_index: int) -> None:
        """
        Feeds data from the previous timestep into the agent allowing it
        to adjust it's strategy.

        Parameters
        ----------
        last_round_profit: int
            A positive integer representing the profit the agent
            made in the previous timestep.
        identity_index: int
            A positive integer that holds the index in the list corresponding to
            the current agent.

        Raises
        ------
        NotImplementedError
            If concrete class does not override method.

        """
        if last_round_profit < 20:
            self.lowest_price = True
