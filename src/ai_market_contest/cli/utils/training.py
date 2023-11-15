import shutil
from typing import Union

import ray
from ray.rllib import agents
from ray.rllib.agents.trainer import Trainer  # type: ignore
from ray.tune.logger import pretty_print  # type: ignore
from ray.tune.registry import register_env

from ai_market_contest.agent import Agent  # type: ignore
from ai_market_contest.environment import Market


def agent_dict_to_list(agent_dict: dict[str, int], env: Market) -> list[int]:
    agent_values: list[int] = []
    for agent_name in env.agents:
        if agent_name in agent_dict:
            agent_values.append(agent_dict[agent_name])
        else:
            raise ValueError(f"Agent {agent_name} not found in agent_dict")
    return agent_values


def get_agent_price_dict(
    agents: list[Union[Agent, Trainer]],
    env: Market,
    last_round_prices: dict[str, int],
) -> dict[str, int]:
    agent_dict: dict[str, int] = {}
    last_round_prices_list = agent_dict_to_list(last_round_prices, env)
    observations = {agent_name: last_round_prices_list for agent_name in env.agents}

    for index, (agent, agent_name) in enumerate(zip(agents, env.agents)):
        if isinstance(agent, Trainer):
            agent_dict[agent_name] = agent.compute_actions(observations)["player_0"]
        else:
            agent_dict[agent_name] = agent.policy(last_round_prices_list, index)

    return agent_dict


def train(env):
    ray.init(ignore_reinit_error=True)

    register_env("marketplace", lambda x: env)

    config = agents.dqn.DEFAULT_CONFIG.copy()
    config.update({"num_workers": 1})

    trainer = agents.dqn.DQNTrainer(env="marketplace")

    chkpt_root = "tmp/exa"
    shutil.rmtree(chkpt_root, ignore_errors=True, onerror=None)

    for _ in range(800):
        result = trainer.train()
        print(pretty_print(result))

    trainer.save(chkpt_root)
