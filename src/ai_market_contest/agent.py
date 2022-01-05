from ray.rllib.policy.policy import Policy
from ray.rllib.utils.typing import TrainerConfigDict, TensorStructType, TensorType
from typing import List, Union, Optional, Dict
from ai_market_contest.typing.types import Price  # type: ignore
import numpy as np
import gym  # type: ignore


class Agent(Policy):
    """
    Agent interface - an agent represents a firm selling a product in the market.

    An agent encapsulates the users private pricing strategy.

    The user is free to implement this interface in order to test strategies.
    As is standard for ML models, it uses the policy-update format.
    For those not familiar with policy-update, see the comments on each function.
    """

    def __init__(self, observation_space=None, action_space=None, config={}):
        super().__init__(observation_space, action_space, config)

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def compute_actions(
        self,
        obs_batch: Union[List[TensorStructType], TensorStructType],
        state_batches: Optional[List[TensorType]] = None,
        prev_action_batch: Union[List[TensorStructType], TensorStructType] = None,
        prev_reward_batch: Union[List[TensorStructType], TensorStructType] = None,
        info_batch: Optional[Dict[str, list]] = None,
        episodes: Optional[List["Episode"]] = None,
        explore: Optional[bool] = None,
        timestep: Optional[int] = None,
        **kwargs
    ):
        identity_index: int = 0
        action_batch: List[Price] = []
        for agent_index in range(len(obs_batch)):
            obs = obs_batch[agent_index]
            prices_list: List[Price] = []
            for index in range(100, len(obs) + 1, 100):
                prices_list.append(np.where(obs[index - 100 : index] == 1)[0][0])
            info = info_batch[agent_index]
            if info == 0:
                if info[agent_index] == 0:
                    action_batch.append(self.get_initial_price())
                else:
                    action_batch.append(prev_action_batch[agent_index])
                continue
            identity_index: int = info["identity_index"]
            self.update(prev_action_batch[agent_index], identity_index)
            action_batch.append(self.policy(prices_list, identity_index))

        return (action_batch, [], {})

    def learn_on_batch(self, samples):
        pass

    def update_target(self):
        return True
