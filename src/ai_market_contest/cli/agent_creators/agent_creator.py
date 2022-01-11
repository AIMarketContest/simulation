import pathlib
from typing import List

from ai_market_contest.cli.cli_config import AGENTS_DIR_NAME, CONFIG_FILENAME


class AgentCreator:
    def __init__(self, proj_dir: pathlib.Path, agent_names: List[str]):
        self.agents = agent_names
        self.proj_dir = proj_dir
        self.agents_dir = self.proj_dir / AGENTS_DIR_NAME
        self.agents_config_file = self.agents_dir / CONFIG_FILENAME
