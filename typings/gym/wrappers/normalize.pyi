"""
This type stub file was generated by pyright.
"""

import gym

class RunningMeanStd:
    def __init__(self, epsilon=..., shape=...) -> None:
        ...
    
    def update(self, x): # -> None:
        ...
    
    def update_from_moments(self, batch_mean, batch_var, batch_count): # -> None:
        ...
    


def update_mean_var_count_from_moments(mean, var, count, batch_mean, batch_var, batch_count): # -> tuple[Unknown, Unknown, Unknown]:
    ...

class NormalizeObservation(gym.core.Wrapper):
    def __init__(self, env, epsilon=...) -> None:
        ...
    
    def step(self, action): # -> tuple[Unknown | Any, Unknown, Unknown, Unknown]:
        ...
    
    def reset(self): # -> Any:
        ...
    
    def normalize(self, obs):
        ...
    


class NormalizeReward(gym.core.Wrapper):
    def __init__(self, env, gamma=..., epsilon=...) -> None:
        ...
    
    def step(self, action): # -> tuple[Unknown, Any | Unknown, Unknown, Unknown]:
        ...
    
    def normalize(self, rews):
        ...
    


