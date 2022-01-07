import pathlib  # type: ignore
from typing import Any, Dict, List, Tuple  # type: ignore

import gym  # type: ignore
from ray.rllib.agents.registry import get_trainer_class  # type: ignore
from ray.tune.logger import pretty_print  # type: ignore
from ray.tune.registry import register_env  # type: ignore

from ai_market_contest.agent import Agent  # type: ignore
from rllib.agents.trainer import Trainer  # type: ignore


class AgentEvaluator:
    def __init__(
        self,
        env: gym.Environment,
        naive_agents_map: Dict[str, Agent],
        naive_agents_counts: Dict[Agent, Any],
        agents: Dict[str, pathlib.Path],
        op_algorithm: str,
    ):
        self.env = env
        self.naive_agents_map = naive_agents_map
        i = 0

        self.trainers = {}
        for agent_name, checkpoint_path in agents.items():
            trainer_cls: Trainer = get_trainer_class(op_algorithm)
            new_trainer: Trainer = trainer_cls()
            new_trainer.restore(checkpoint_path)
            self.trainers[agent_name] = new_trainer

    def evaluate(self) -> None:
        done = False
        action_arr = []
        rewards_arr = []
        obs = self.env.reset()
        while not done:
            actions = {}
            observed_actions = {}
            for naive_agent_str, naive_agent in self.naive_agents_map.items():
                action = naive_agent.policy(obs[naive_agent_str], 0)
                actions[naive_agent_str] = action

            for agent_name, trainer in self.trainers.items():
                action = trainer.compute_action(obs[agent_name])
                actions[agent_name] = action

            obs, rewards, dones, infos = env.step(actions)
            done = dones["__all__"]
            action_arr.append(actions)
            rewards_arr.append(rewards)

        return action_arr, reward_arr
