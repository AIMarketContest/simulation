import configparser
import sys
from pathlib import Path

from ai_market_contest.cli.cli_config import CONFIG_FILENAME
from ai_market_contest.cli.utils.filesystemutils import (
    check_config_file_exists,
    check_directory_exists,
)


def check_agent_is_initialised(agent_dir: Path) -> bool:
    config_file: Path = agent_dir / CONFIG_FILENAME
    check_config_file_exists(config_file)
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    try:
        initialised: bool = config["training"]["initialised"] == "True"
    except KeyError:
        print("Error: Config file missing initialised attribute")
        sys.exit(1)
    return initialised


def check_directory_exists_for_agent(chosen_agent: str, chosen_agent_dir: Path) -> None:
    error_msg: str = f"Error: no directory exists for {chosen_agent}"
    check_directory_exists(chosen_agent_dir, error_msg)
