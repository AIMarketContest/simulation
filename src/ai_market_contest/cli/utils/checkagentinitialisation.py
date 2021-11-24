import configparser
import pathlib
import sys
from ai_market_contest.cli.cli_config import CONFIG_FILENAME
from ai_market_contest.cli.utils.filesystemutils import check_config_file_exists


def check_agent_is_initialised(agent_dir: pathlib.Path):
    config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    check_config_file_exists(config_file)
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    try:
        initialised: bool = config["training"]["initialised"] == "True"
    except KeyError:
        print("Error: Config file missing initialised attribute")
        sys.exit(1)
    return initialised
