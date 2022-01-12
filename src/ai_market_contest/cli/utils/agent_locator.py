from abc import ABCMeta
import importlib.util
import pathlib
from types import ModuleType

import dill

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
        if "-opponent" in agent_name:
            agent_name = agent_name[: -len("-opponent")]
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
