from ray.rllib import agents
from ray.tune.registry import register_env

from ai_market_contest.agents.random_agent import RandomAgent
from ai_market_contest.demandfunctions.fixed_lowest_takes_all_demand_function import (
    LowestTakesAllDemandFunction,
)
from ai_market_contest.environment import Market
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)

num_agents: int = 2
agent_name_maker: AgentNameMaker = SequentialAgentNameMaker(5)
env = Market(num_agents, LowestTakesAllDemandFunction(99), 10, agent_name_maker)

test_agents = [RandomAgent()]

register_env(
    "marketplace",
    lambda x: env,
)

config = agents.dqn.DEFAULT_CONFIG.copy()
config.update(
    {
        "num_workers": 1,
    }
)

trainer = agents.dqn.DQNTrainer(env="marketplace")


# run until episode ends

action_arr = []
rewards_arr = []

obs = env.reset()
done = False
while not done:
    actions = {}
    actions["player_0"] = trainer.compute_action(obs["player_1"])
    actions["player_1"] = test_agents[0].policy(obs)

    obs, rewards, dones, infos = env.step(actions)
    done = dones["__all__"]
    action_arr.append(actions)
    rewards_arr.append(rewards)

print(action_arr)
print("")
print(rewards_arr)
