import pathlib

from ai_market_contest.cli.cli_config import TRAINED_AGENTS_DIR_NAME
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent


class ExistingAgentVersion:
    def __init__(self, agent: ExistingAgent, version: str):
        self.agent = agent
        self.version = version
        self.dir = agent.get_dir() / TRAINED_AGENTS_DIR_NAME / version

    def get_agent_name(self) -> str:
        return self.agent.get_name()

    def get_agent_dir(self) -> pathlib.Path:
        return self.agent.get_dir()

    def was_agent_initialised(self) -> bool:
        return self.agent.is_initialised()

    def get_dir(self) -> pathlib.Path:
        return self.dir
