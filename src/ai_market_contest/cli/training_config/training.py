import shutil
from typing import List, Dict

import ray
from ray.rllib import agents  # type: ignore
from ray.tune.logger import pretty_print  # type: ignore
from ray.tune.registry import register_env  # type: ignore

from ai_market_contest.environment import Market


def agent_dict_to_list(agent_dict: Dict[str, int], env: Market) -> List[int]:
    agent_values: List[int] = []
    for agent_name in env.possible_agents:
        if agent_name in agent_dict:
            agent_values.append(agent_dict[agent_name])
        else:
            raise ValueError(f"Agent {agent_name} not found in agent_dict")
    return agent_values


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
