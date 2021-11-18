from typing import Any, List, Optional, Union

import dm_env
from mava.wrappers import (PettingZooAECEnvWrapper,
                           PettingZooParallelEnvWrapper)

from environment import init_env, Environment
from demandfunctions.fixed_demand_function import FixedDemandFunction

def make_environment(
    evaluation: bool = False,
    env_type: str = "parallel",
    env_module: Environment = init_env(100, FixedDemandFunction(), 10),
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

    environment: Optional[dm_env.Environment] = None

    if env_type == "parallel":
        env = env_module.parallel_env(**kwargs)  # type: ignore
        environment = PettingZooParallelEnvWrapper(env)
    elif env_type == "sequential":
        env = env_module.env(**kwargs)  # type: ignore
        environment = PettingZooAECEnvWrapper(env)

    if random_seed and hasattr(environment, "seed"):
        environment.seed(random_seed)

    return environment
