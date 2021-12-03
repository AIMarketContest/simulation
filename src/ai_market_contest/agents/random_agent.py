import random

from ai_market_contest.agent import Agent


class RandomAgent(Agent):
    """
    An agent which returns a random price.
    """

    def compute_actions(
        self,
        obs_batch,
        state_batches=None,
        prev_action_batch=None,
        prev_reward_batch=None,
        info_batch=None,
        episodes=None,
    ):

        return [random.randint(0, 99) for _ in obs_batch], [], {}
    
    def learn_on_batch(self, samples):
        pass

    def __str__(self):
        return "RandomAgent()"
