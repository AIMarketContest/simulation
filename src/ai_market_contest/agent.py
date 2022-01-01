from ray.rllib.policy.policy import Policy
from ray.rllib.utils.typing import TrainerConfigDict
import gym


class Agent(Policy):
    """
    Agent interface - an agent represents a firm selling a product in the market.

    An agent encapsulates the users private pricing strategy.

    The user is free to implement this interface in order to test strategies.
    As is standard for ML models, it uses the policy-update format.
    For those not familiar with policy-update, see the comments on each function.
    """

    def __init__(
        self,
        observation_space: gym.env = None,
        action_space: gym.env = None,
        config: TrainerConfigDict = {}
    ):
        super().__init__(observation_space, action_space, config)

    def set_initial_price(self) -> float:
        raise NotImplementedError

    def set_price(
        self, last_round_all_agents_prices: List[float], identity_index: int
    ) -> float:
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
            discretised within [0,1].

        Raises
        ------
        NotImplementedError
            If concrete class does not override method.
        """
        raise NotImplementedError

    def get_initial_state(self):
        return self.set_initial_price()

    def compute_actions(
        self,
        obs_batch,
        state_batches=None,
        prev_action_batch=None,
        prev_reward_batch=None,
        info_batch=None,
        episodes=None,
    ):
        identity_index = 0
        if info_batch:
            info = info_batch[0]
            identity_index = info["identity_index"]
        return (
            [self.set_price(prices_list, identity_index) for prices_list in obs_batch],
            [],
            {},
        )

    def learn_on_batch(self, samples):
        pass
