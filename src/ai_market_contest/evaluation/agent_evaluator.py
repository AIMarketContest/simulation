from typing import Any, Dict, Tuple  # type: ignore

import gym  # type: ignore
from ray.rllib.agents.registry import get_trainer_class  # type: ignore
from ray.rllib.agents.trainer import Trainer  # type: ignore
from ray.tune.registry import register_env  # type: ignore

from ai_market_contest.agent import Agent  # type: ignore
from ai_market_contest.cli.utils.agent_locator import AgentLocator  # type: ignore
from ai_market_contest.cli.utils.checkpoint_locator import (
    get_checkpoint_path,  # type: ignore
)
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,  # type: ignore
)
from ai_market_contest.training.agent_name_maker import AgentNameMaker  # type: ignore


class AgentEvaluator:
    def __init__(
        self,
        env: gym.Env,
        agent_locator: AgentLocator,
        naive_agents_counts: Dict[str, Any],
        agents: Dict[str, ExistingAgentVersion],
        op_algorithm: str,
        agent_name_maker: AgentNameMaker,
    ):
        register_env("marketplace", lambda x: env)
        self.env = env
        self.naive_agents_map: Dict[str, Tuple[Agent, int]] = {}
        index: int = 0
        self.agent_name_map = {}
        for agent_name, count in naive_agents_counts.items():
            for i in range(count):
                indexed_agent_name: str = f"{agent_name}_{str(i)}"
                self.naive_agents_map[indexed_agent_name] = agent_locator.get_agent(
                    agent_name
                )
                self.agent_name_map[indexed_agent_name] = agent_name_maker.get_name(
                    index
                )
                index += 1

        self.trainers = {}
        for agent_name, chosen_agent_version in agents.items():
            trainer_cls: Trainer = get_trainer_class(op_algorithm)
            new_trainer: Trainer = trainer_cls(
                env="marketplace", config={"num_workers": 1, "explore": False}
            )
            checkpoint_path: str = get_checkpoint_path(
                chosen_agent_version.get_dir(), True
            )
            new_trainer.restore(checkpoint_path)
            self.trainers[agent_name] = new_trainer
            self.agent_name_map[agent_name] = agent_name_maker.get_name(index)
            self.reversed_agent_name_map[agent_name_maker.get_name(index)] = agent_name
            index += 1

    def evaluate(self) -> None:
        done = False
        action_arr = []
        rewards_arr = []
        obs = self.env.reset()
        while not done:
            actions = {}
            observed_actions = {}
            for naive_agent_str, naive_agent in self.naive_agents_map.items():
                env_agent_name = self.agent_name_map[naive_agent_str]
                action = naive_agent.policy(obs[env_agent_name], 0)
                actions[naive_agent_str] = action
                observed_actions[env_agent_name] = action

            for agent_name, trainer in self.trainers.items():
                env_agent_name = self.agent_name_map[agent_name]
                action = trainer.compute_action(obs)
                actions[agent_name] = action
                observed_actions[env_agent_name] = action

            obs, observed_rewards, dones, infos = env.step(observed_actions)
            done = dones["__all__"]
            action_arr.append(actions)
            rewards = {
                self.reversed_agent_name_map[env_agent_name]: reward
                for (env_agent_name, reward) in observed_rewards
            }
            rewards_arr.append(rewards)

        return action_arr, reward_arr
