"""
This type stub file was generated by pyright.
"""

import gym

class RescaleAction(gym.ActionWrapper):
    r"""Rescales the continuous action space of the environment to a range [min_action, max_action].

    Example::

        >>> RescaleAction(env, min_action, max_action).action_space == Box(min_action, max_action)
        True

    """
    def __init__(self, env, min_action, max_action) -> None:
        ...
    
    def action(self, action): # -> Any:
        ...
    


