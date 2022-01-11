import ast
import configparser
import pathlib
import sys
from typing import Dict, List

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    CONFIG_FILENAME,
    HASH_LENGTH,
    PROJ_DIR_NAME,
)
from ai_market_contest.cli.utils.filesystemutils import check_config_file_exists
from ai_market_contest.cli.utils.processmetafile import get_trained_agent_metadata


def get_custom_agent_names(proj_dir: pathlib.Path) -> List[str]:
    config: configparser.ConfigParser = configparser.ConfigParser()
    config_file: pathlib.Path = proj_dir / AGENTS_DIR_NAME / CONFIG_FILENAME
    check_config_file_exists(config_file)
    config.read(config_file)
    try:
        agents: List[str] = ast.literal_eval(config["agents"]["customagents"])
    except KeyError:
        print("Error: config file needs an agents attribute")
        sys.exit(1)
    return agents


def get_rllib_agents(proj_dir: pathlib.Path) -> List[str]:
    config: configparser.ConfigParser = configparser.ConfigParser()
    config_file: pathlib.Path = proj_dir / AGENTS_DIR_NAME / CONFIG_FILENAME
    check_config_file_exists(config_file)
    config.read(config_file)
    try:
        agents: List[str] = ast.literal_eval(config["agents"]["rllibagents"])
    except KeyError:
        print("Error: config file needs an agents attribute")
        sys.exit(1)
    return agents


def get_trained_agents(agent_dir: pathlib.Path) -> List[str]:
    agent_config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    check_config_file_exists(agent_config_file)
    config.read(agent_config_file)
    try:
        trained_agents: List[str] = ast.literal_eval(
            config["training"]["trained-agents"]
        )
    except KeyError:
        print("Error: Config file needs a trained-agents attribute")
        sys.exit(1)
    return trained_agents


def get_trained_agents_info(
    trained_agents: List[str], agent_dir: pathlib.Path
) -> List[str]:
    trained_agents_information: Dict[str, str] = {}
    trained_agent: str
    for trained_agent in trained_agents:
        (agent_hash, time, msg, parent_hash) = get_trained_agent_metadata(
            agent_dir, trained_agent
        )
        shortened_hash: str = agent_hash[:HASH_LENGTH]
        trained_agents_information[f"\n{shortened_hash} {str(time)} {msg}"] = agent_hash
    return trained_agents_information


def add_trained_agent_to_config_file(agent_dir: pathlib.Path, trained_agent_name: str):
    config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    check_config_file_exists(config_file)
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    try:
        trained_agents: list[str] = ast.literal_eval(
            config["training"]["trained-agents"]
        )
    except KeyError:
        print("Error: Config file needs a trained-agents attribute")
        sys.exit(1)

    trained_agents.append(trained_agent_name)
    config["training"]["trained-agents"] = str(trained_agents)
    with config_file.open("w") as c_file:
        config.write(c_file)
