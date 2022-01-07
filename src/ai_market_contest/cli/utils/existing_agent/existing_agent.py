import pathlib

from ai_market_contest.cli.cli_config import AGENTS_DIR_NAME
from ai_market_contest.cli.utils.agent_check_utils import (
    check_agent_is_initialised,
    check_directory_exists_for_agent,
)


class ExistingAgent:
    def __init__(self, agent_name, project_directory: pathlib.Path):
        self.agent_name: str = agent_name
        self.agent_directory: pathlib.Path = (
            project_directory / AGENTS_DIR_NAME / self.get_name()
        )
        check_directory_exists_for_agent(self.agent_name, self.agent_directory)
        self.initialised: bool = check_agent_is_initialised(self.agent_directory)

    def get_name(self) -> str:
        return self.agent_name

    def get_dir(self) -> pathlib.Path:
        return self.agent_directory

    def is_initialised(self) -> bool:
        return self.initialised
