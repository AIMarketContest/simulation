from typing import List
from ai_market_contest.agent import Agent

from ai_market_contest.environment import Market
from ray.rllib.policy.policy import Policy


def run_contest(env: Market, agents: dict[Policy, str]):
    agent_sales: dict[Policy, list[float]] = {
        agent_name: [] for agent_name in agents.keys
    }
    previous_actions: dict[str, float] = {}
    current_actions: dict[str, float] = {}

    dones: dict[Policy, bool] = {agent: False for agent in agents.keys}
    obs = env.reset()
    for agent, agent_id in agents:
        previous_actions[agent_id] = agent.compute_action(obs)
    obs, rewards, dones, infos = env.step(current_actions)

    while not all(dones.values()):
        for agent, agent_id in agents:
            current_actions[agent_id] = agent.compute_action(
                obs,
                previous_actions=previous_actions[agent_id],
                prev_reward=rewards[agent],
                info=infos,
            )
            agent_sales[agent].append(rewards[agent_id])

        previous_actions = current_actions
        obs, rewards, dones, infos = env.step(previous_actions)
