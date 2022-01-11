import pathlib
import numpy as np

from ray.rllib.policy.policy import PolicySpec
import ray.rllib.agents.dqn as dqn
from ai_market_contest.agents.random_agent import RandomAgent
from ai_market_contest.demandfunctions.fixed_lowest_takes_all_demand_function import (
    LowestTakesAllDemandFunction,
)

from ai_market_contest.demandfunctions.gaussian_demand_function import (
    GaussianDemandFunction,
)

from ray.tune.registry import register_env  # type: ignore

from ai_market_contest.environment import Market
from ai_market_contest.test_agent import TestAgent
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.agent_trainer import AgentTrainer
from ai_market_contest.training.policy_selector import PolicySelector
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)
from ai_market_contest.evaluation.one_hot_encoder import OneHotEncoder  # type: ignore
from ai_market_contest.evaluation.graphing import plot_average_step, graph_profits, graph_cumulative_profits  # type: ignore

num_agents: int = 5
agent_name_maker: AgentNameMaker = SequentialAgentNameMaker(num_agents)


num_self_play_agents = 0
demand_function = GaussianDemandFunction
training_duration: int = 50
env = Market(num_agents, demand_function(), training_duration, agent_name_maker)

random_agent_spec = PolicySpec(policy_class=RandomAgent)
test_agent_spec = PolicySpec(policy_class=TestAgent)

naive_agents_counts = {"random-agent": num_agents - num_self_play_agents - 1}
ps = PolicySelector(
    "test-agent",
    self_play_number=num_self_play_agents,
    naive_agents_counts=naive_agents_counts,
)
config = {
    "num_workers": 0,
    "prioritized_replay": False,
    "multiagent": {
        "policies_to_train": ["test-agent"],
        "policies": {
            "random-agent": random_agent_spec,
            "test-agent": test_agent_spec,
        },
        "policy_mapping_fn": ps.get_select_policy_function(),
    },
}

agent_trainer = AgentTrainer(env, config, restored=False, checkpoint_path=None)
agent_trainer.train(20, True)
path = pathlib.Path.cwd()
agent_trainer.save(path)
# agent_trainer = AgentTrainer(
#     env,
#     config,
#     restored=True,
#     checkpoint_path=str((path / "checkpoint_000001/checkpoint-1").resolve()),
# )
# agent_trainer.train(1, True)
# agent_trainer.save(path)
agent_name_maker = SequentialAgentNameMaker(3)
env = Market(3, demand_function(), training_duration, agent_name_maker)
register_env("marketplace", lambda x: env)
done = False
action_arr = []
rewards_arr = {"random-agent_1": [], "random-agent_2": [], "q-agent": []}
obs = env.reset()
print(obs)
infos = {
    "player_0": 0,
    "player_1": 0,
    "player_2": 0,
}

ps = PolicySelector(
    "test-agent",
    self_play_number=0,
    naive_agents_counts={"random-agent": 2},
)

config = {
    "num_workers": 1,
    "explore": False,
    "prioritized_replay": False,
    "multiagent": {
        "policies_to_learn": ["test-agent"],
        "policies": {"random-agent": random_agent_spec, "test-agent": test_agent_spec},
        "policy_mapping_fn": ps.get_select_policy_function(),
    },
}
# new_trainer = dqn.DQNTrainer(config=config, env="marketplace")
# new_trainer.restore(str((path / "checkpoint_000001/checkpoint-1").resolve()))
observed_rewards = {
    "player_0": 0,
    "player_1": 0,
    "player_2": 0,
}
observed_actions = {
    "player_0": 0,
    "player_1": 0,
    "player_2": 0,
}

naive_agents_map = {"random-agent_1": RandomAgent(), "random-agent_2": RandomAgent()}

agent_name_map = {
    "random-agent_1": "player_0",
    "random-agent_2": "player_1",
    "q-agent": "player_2",
}
trainers = {"q-agent": ("test-agent", agent_trainer.get_trainer())}
reversed_agent_name_map = {
    "player_0": "random-agent_1",
    "player_1": "random-agent_2",
    "player_2": "q-agent",
}
OHE = OneHotEncoder([i for i in range(100)])
while not done:
    actions = {}
    for naive_agent_str, naive_agent in naive_agents_map.items():
        env_agent_name = agent_name_map[naive_agent_str]
        action = naive_agent.policy(
            obs[env_agent_name],
            identity_index=0,
        )
        actions[naive_agent_str] = action
        observed_actions[env_agent_name] = action

    for agent_name, (agent_cls_name, trainer) in trainers.items():
        env_agent_name = agent_name_map[agent_name]
        [action], _, _ = trainer.get_policy(agent_cls_name).compute_actions(
            np.array([OHE.one_hot_encode(obs[env_agent_name])]),
            info_batch=[infos[env_agent_name]],
            prev_action_batch=[observed_actions[env_agent_name]],
            prev_reward_batch=[observed_rewards[env_agent_name]],
        )
        actions[agent_name] = action
        observed_actions[env_agent_name] = action

    obs, observed_rewards, dones, infos = env.step(observed_actions)
    done = dones["__all__"]
    action_arr.append(actions)
    rewards = {
        reversed_agent_name_map[env_agent_name]: reward
        for (env_agent_name, reward) in observed_rewards.items()
    }
    for agent_name, reward in rewards.items():
        rewards_arr[agent_name].append(reward)
plot_average_step(rewards_arr)
graph_profits(rewards_arr)
graph_cumulative_profits(rewards_arr)
