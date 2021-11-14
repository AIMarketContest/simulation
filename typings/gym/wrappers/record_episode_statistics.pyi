"""
This type stub file was generated by pyright.
"""

from typing import Dict

import gym
from agent import Agent
from environment import Environment

class RecordEpisodeStatistics(gym.Wrapper):
    def __init__(self, env: Environment, deque_size: int = ...) -> None: ...
    def reset(self, **kwargs): ...
    def step(self, action: Dict[Agent, float]): ...
