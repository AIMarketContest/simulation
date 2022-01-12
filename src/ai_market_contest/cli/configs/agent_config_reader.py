import pathlib
from ast import literal_eval
from configparser import ConfigParser
from typing import List, Optional

from ai_market_contest.cli.cli_config import CONFIG_FILENAME
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)


class AgentConfigReader:
    def __init__(self, agent_version: ExistingAgentVersion):
        self.config_parser: ConfigParser = ConfigParser()
        self.agent_config_file: pathlib.Path = (
            agent_version.get_agent_dir() / CONFIG_FILENAME
        )
        self.config_parser.optionxform = str
        self.config_parser.read(self.agent_config_file)

    def get_agent_type(self) -> str:
        return self.config_parser["general"]["type"]

    def get_rllib_type(self) -> Optional[str]:
        if self.get_agent_type() == "rllib":
            return self.config_parser["rllib"]["agent_type"]
        return None

    def get_initial_hash(self) -> str:
        return self.config_parser["training"]["initial_hash"]

    def get_trained_agents(self) -> list[str]:
        return literal_eval(self.config_parser["training"]["trained_agents"])

    def agent_is_initialised(self) -> bool:
        return literal_eval(self.config_parser["training"]["initialised"])
