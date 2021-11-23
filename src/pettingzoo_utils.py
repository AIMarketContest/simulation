from typing import Any, List, Optional, Union

import dm_env
from mava.wrappers import PettingZooAECEnvWrapper, PettingZooParallelEnvWrapper

from ai_market_contest.agents.fixed_agent import FixedAgent
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction
from ai_market_contest.environment import Environment, init_env


def make_environment(
    evaluation: bool = False,
    env_type: str = "parallel",
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
        env = init_env([FixedAgent()], FixedDemandFunction(), 10)  # type: ignore
        environment = PettingZooParallelEnvWrapper(env)
    elif env_type == "sequential":
        env = env_module.env(**kwargs)  # type: ignore
        environment = PettingZooAECEnvWrapper(env)

    if random_seed and hasattr(environment, "seed"):
        environment.seed(random_seed)

    return environment
