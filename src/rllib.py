from ray.tune.registry import register_env
from ray.rllib.env import ParallelPettingZooEnv
from ray.rllib import agents

from ai_market_contest.environment import init_env
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction
from ray.tune.logger import pretty_print


register_env(
    "marketplace",
    lambda x: ParallelPettingZooEnv(init_env(10, FixedDemandFunction(1), 5)),
)

trainer = agents.dqn.DQNTrainer(env="marketplace")


for i in range(1000):
   # Perform one iteration of training the policy with PPO
   result = trainer.train()
   print(pretty_print(result))

   if i % 100 == 0:
       checkpoint = trainer.save()
       print("checkpoint saved at", checkpoint)