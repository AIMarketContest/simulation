from ray.tune.registry import register_env
from ray.rllib.env import ParallelPettingZooEnv

from ai_market_contest.environment import init_env
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction

register_env(
    "marketplace",
    lambda x: ParallelPettingZooEnv(init_env(10, FixedDemandFunction(1), 5)),
)
