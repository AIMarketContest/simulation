"""
This type stub file was generated by pyright.
"""

from gym import ObservationWrapper

class TimeAwareObservation(ObservationWrapper):
    r"""Augment the observation with current time step in the trajectory.

    .. note::
        Currently it only works with one-dimensional observation space. It doesn't
        support pixel observation space yet.

    """
    def __init__(self, env) -> None:
        ...
    
    def observation(self, observation):
        ...
    
    def step(self, action):
        ...
    
    def reset(self, **kwargs):
        ...
    


