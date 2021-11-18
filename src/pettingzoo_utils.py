import importlib
from typing import Any, List, Optional, Union

import dm_env
import numpy as np
import supersuit
from supersuit import black_death_v1
from src.environment import Environment
from mava.wrappers import (
    ParallelEnvWrapper,
    PettingZooAECEnvWrapper,
    PettingZooParallelEnvWrapper,
    SequentialEnvWrapper,
)


def make_environment(
    evaluation: bool = False,
    env_type: str = "parallel",
    env_module: Environment = Environment(),
    env_preprocess_wrappers: Optional[List] = [(black_death_v1, None)],
    random_seed: Optional[int] = None,
    **kwargs: Any,
) -> dm_env.Environment:
    """Wraps an Pettingzoo environment.
    Args:
        env_module: the custom Pettinzoo environment used for the simulation
        evaluation: bool, to change the behaviour during evaluation.
    Returns:
        A Pettingzoo environment wrapped as a DeepMind environment.
    """
    del evaluation

    if env_type == "parallel":
        env = env_module.parallel_env(**kwargs)  # type: ignore
        # wrap parallel environment
        environment = PettingZooParallelEnvWrapper(
            env, env_preprocess_wrappers=env_preprocess_wrappers
        )
    elif env_type == "sequential":
        env = env_module.env(**kwargs)  # type: ignore
        # wrap sequential environment
        environment = PettingZooAECEnvWrapper(
            env, env_preprocess_wrappers=env_preprocess_wrappers
        )

    if random_seed and hasattr(environment, "seed"):
        environment.seed(random_seed)

    return environment