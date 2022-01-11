import pathlib
import pickle
import sys
from typing import Dict

import gym

from ai_market_contest.agent import Agent
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.pklfileutils import write_pkl_file
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.agent_trainer import AgentTrainer


class CustomAgentTrainer(AgentTrainer):
    def __init__(
        self,
        env: gym.Env,
        agent_version: ExistingAgentVersion,
        naive_agents_counts: Dict[str, int],
        self_play_num: int,
        agent_locator: AgentLocator,
        agent_name_maker: AgentNameMaker,
    ):
        sys.path.insert(0, str(agent_version.get_dir().resolve()))
        self.env = env
        self.agent_version = agent_version
        training_agent_cls: Agent = agent_locator.get_agent(
            agent_version.get_agent_name()
        )
        if agent_version.was_agent_initialised():
            training_agent: Agent = agent_version.get_agent_from_pickle()
        else:
            training_agent: Agent = training_agent_cls()
        self.agents: Dict[str, Agent] = {agent_name_maker.get_name(0): training_agent}
        self.agent_name_maker = agent_name_maker
        index: int = 1
        print(self.agents["player_0"])
        for _ in range(self_play_num):
            self.agents[agent_name_maker.get_name(index)] = training_agent_cls()
            index += 1
        for naive_agent_name, count in naive_agents_counts.items():
            for _ in range(count):
                naive_agent = agent_locator.get_agent(naive_agent_name)
                self.agents[agent_name_maker.get_name(index)] = naive_agent()
                index += 1

    def train(self, epochs: int, print_training: bool):
        for _ in range(epochs):
            done: bool = False
            rewards = {}
            obs = self.env.reset()
            actions = {
                agent_id: agent.get_initial_price()
                for agent_id, agent in self.agents.items()
            }
            while not done:
                obs, rewards, dones, infos = self.env.step(actions)
                prices_list = obs[self.agent_name_maker.get_name(0)]
                for agent_id, agent in self.agents.items():
                    prev_reward = rewards.get(agent_id, 0)
                    identity_index = infos[agent_id]["identity_index"]
                    agent.update(prev_reward, identity_index)
                    actions[agent_id] = agent.policy(prices_list, identity_index)
                done = dones["__all__"]
            if print_training:
                print(rewards)

    def save(self, pickle_dir: pathlib.Path):
        agent = self.agents[self.agent_name_maker.get_name(0)]
        print(agent)
        write_pkl_file(pickle_dir, agent)
