import pathlib
import pickle
import sys

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import AGENT_PKL_FILENAME, TRAINED_AGENTS_DIR_NAME
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent


class ExistingAgentVersion:
    def __init__(self, agent: ExistingAgent, version: str, is_rllib: bool):
        self.agent = agent
        self.dir = agent.get_dir() / TRAINED_AGENTS_DIR_NAME / version
        self.is_rllib = is_rllib

    def get_agent_name(self) -> str:
        return self.agent.get_name()

    def get_agent_dir(self) -> pathlib.Path:
        return self.agent.get_dir()

    def was_agent_initialised(self) -> bool:
        return self.agent.is_initialised()

    def get_dir(self) -> pathlib.Path:
        return self.dir

    def is_rllib_agent(self) -> bool:
        return self.is_rllib

    def get_agent_from_pickle(self) -> Agent:
        pickle_file: pathlib.Path = self.get_dir() / AGENT_PKL_FILENAME
        with pickle_file.open("rb") as p_file:
            agent: Agent = pickle.load(p_file)
        return agent
