"""
This type stub file was generated by pyright.
"""

from gym import ObservationWrapper

class ResizeObservation(ObservationWrapper):
    r"""Downsample the image observation to a square image."""
    def __init__(self, env, shape) -> None: ...
    def observation(self, observation): ...
