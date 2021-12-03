from typing import List
from ai_market_contest.agent import Agent

from ai_market_contest.environment import Market
from ray.rllib.policy.policy import Policy
from ray.tune.registry import register_env


def run_contest(env: Market, agents: dict[Policy, str]):

    agent_sales: dict[Policy, list[float]] = {
        agent_name: [] for agent_name in agents.keys()
    }
    previous_actions: dict[str, float] = {}
    current_actions: dict[str, float] = {}

    dones: dict[Policy, bool] = {agent: False for agent in agents.keys()}
    obs = env.reset()
    for agent, agent_id in agents.items():
        previous_actions[agent_id], _ = agent.compute_actions(obs)[0]
    obs, rewards, dones, infos = env.step(previous_actions)

    while not all(dones.values()):
        for agent, agent_id in agents.items():
            current_actions[agent_id], _ = agent.compute_actions(
                obs,
                prev_action_batch=previous_actions[agent_id],
                prev_reward_batch=rewards[agent_id],
                info_batch=infos,
            )[0]
            agent_sales[agent].append(rewards[agent_id])

        previous_actions = current_actions
        obs, rewards, dones, infos = env.step(previous_actions)

    return agent_sales
