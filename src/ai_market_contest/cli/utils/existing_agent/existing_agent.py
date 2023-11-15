import pathlib
from ast import literal_eval
from typing import Any, Optional

from ai_market_contest.cli.cli_config import (
    AGENTS_DIR_NAME,
    CONFIG_FILENAME,
    HASH_LENGTH,
)
from ai_market_contest.cli.utils.agent_check_utils import (
    check_agent_is_initialised,
    check_directory_exists_for_agent,
)
from ai_market_contest.cli.utils.config_utils import get_config_dict
from ai_market_contest.cli.utils.processmetafile import get_trained_agent_metadata


class ExistingAgent:
    def __init__(self, agent_name: str, project_directory: pathlib.Path):
        self.agent_name: str = agent_name
        self.agent_dir: pathlib.Path = (
            project_directory / AGENTS_DIR_NAME / self.get_name()
        )
        check_directory_exists_for_agent(self.agent_name, self.agent_dir)
        self.initialised: bool = check_agent_is_initialised(self.agent_dir)

    def get_name(self) -> str:
        return self.agent_name

    def get_dir(self) -> pathlib.Path:
        return self.agent_dir

    def is_initialised(self) -> bool:
        return self.initialised

    def get_config(self) -> dict[str, Any]:
        return get_config_dict(self.agent_dir / CONFIG_FILENAME)

    def get_trained_agents_info(self, trained_agents: list[str]) -> dict[str, str]:
        trained_agents_information: dict[str, str] = {}

        for trained_agent in trained_agents:
            (agent_hash, time, msg, _) = get_trained_agent_metadata(
                self.agent_dir, trained_agent
            )
            shortened_hash: str = agent_hash[:HASH_LENGTH]
            trained_agents_information[
                f"{shortened_hash} {str(time)} {msg}"
            ] = agent_hash

        return trained_agents_information

    def get_trained_agents(self) -> Optional[list[str]]:
        try:
            trained_agents: list[str] = literal_eval(
                self.get_config()["training"]["trained-agents"]
            )
            return trained_agents
        except ValueError:
            return

    def get_all_trained_agents_information(self) -> Optional[dict[str, str]]:
        trained_agents: list[str] = self.get_trained_agents()
        if not trained_agents:
            return

        try:
            trained_agents_info: dict[str, str] = self.get_trained_agents_info(
                trained_agents
            )
        except ValueError:
            return

        return trained_agents_info
