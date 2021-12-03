from ai_market_contest.agent import Agent


class FixedAgent(Agent):
    """
    An agent that always returns the same price.
    """

    def __init__(self, price: int = 50):
        self.price = price

    def compute_actions(
        self,
        obs_batch,
        state_batches=None,
        prev_action_batch=None,
        prev_reward_batch=None,
        info_batch=None,
        episodes=None,
    ):

        return [self.price for _ in obs_batch], [], {}

    def __str__(self):
        return f"FixedAgent(price: {self.price})"
