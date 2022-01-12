import importlib.util
import pathlib
import re
from abc import ABCMeta
from types import ModuleType

import gym
from ray.rllib.agents.registry import get_trainer_class
from ray.tune.registry import register_env

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import CUR_AGENTS, TRAINED_PICKLE_FILENAME
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)


class AgentLocator:
    def __init__(self, agents_dir: pathlib.Path):
        self.agents_dir: pathlib.Path = agents_dir

    def get_agent(self, agent_name: str) -> ABCMeta:
        if agent_name in CUR_AGENTS:
            return CUR_AGENTS[agent_name]
        agent_dir: pathlib.Path = self.agents_dir / agent_name
        agent_file: str = agent_dir / (agent_name + ".py")
        spec = importlib.util.spec_from_file_location(agent_name, agent_file)
        if spec.loader is None:
            raise Exception("Error in finding the required agent")
        agent_module: ModuleType = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)  # type: ignore
        agent_cls = getattr(agent_module, agent_name)  # type: ignore
        return agent_cls

    def get_agent_class_or_pickle(self, agent_version: ExistingAgentVersion):
        agent_cls = self.get_agent(agent_version.get_agent_name())
        agent: Agent = agent_cls()

        agent_pickle_path = agent_version.get_dir() / TRAINED_PICKLE_FILENAME
        if agent_pickle_path.exists():
            with open(agent_pickle_path, "rb") as f:
                agent.load(f)

        return agent

    def get_trainer(
        self,
        agent_version: ExistingAgentVersion,
        env: gym.Env,
        agent_config_reader: AgentConfigReader,
    ):
        register_env("marketplace", lambda x: env)
        agent_paths = list(agent_version.get_dir().iter_dir())
        agent_checkpoint_dirs = list(
            filter(lambda x: x.startswith("checkpoint"), agent_paths)
        )
        rllib_type: str = agent_config_reader.get_rllib_type()
        trainer_cls = get_trainer_class(rllib_type)
        trainer = trainer_cls(
            config=trainer_cls.get_default_config(), env="marketplace"
        )
        if agent_checkpoint_dirs:
            agent_checkpoint_dir = agent_checkpoint_dirs[0]
            agent_checkpoints = list(agent_checkpoint_dir.iter_dir())
            agent_checkpoint_files = list(
                filter(lambda x: re.match("checkpoint-[0-9]*", x), agent_checkpoints)
            )
            if agent_checkpoint_files:
                agent_checkpoint_file = agent_checkpoint_files[0]
                with agent_checkpoint_file.open("w") as agent_checkpoint_file:
                    trainer.restore(str(agent_checkpoint_file.resolve()))
        return trainer
