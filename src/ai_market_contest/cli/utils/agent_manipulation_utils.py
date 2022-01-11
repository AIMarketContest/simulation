import ast
import atexit
import configparser
import pathlib
import shutil

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    CONFIG_FILENAME,
)
from ai_market_contest.cli.utils.initialiseagent import create_agent_class


def edit_project_config_file(agent_name: str, proj_dir: pathlib.Path):
    config_file: pathlib.Path = proj_dir / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    agents: list[str] = ast.literal_eval(config["agent"]["agents"])
    if agent_name not in agents:
        agents.append(agent_name)
    config["agent"]["agents"] = str(agents)
    with config_file.open("w") as c_file:
        config.write(c_file)


def remove_agent_dir(agent_name: str, proj_dir: pathlib.Path):
    agents_dir = proj_dir / AGENTS_DIR_NAME
    agent_dir = agents_dir / agent_name
    if agent_dir.is_dir():
        shutil.rmtree(agent_dir)
    config_file: pathlib.Path = proj_dir / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    agents: list[str] = ast.literal_eval(config["agent"]["agents"])
    if agent_name in agents:
        agents.remove(agent_name)
    config["agent"]["agents"] = str(agents)
    with config_file.open("w") as c_file:
        config.write(c_file)


def create_agent(path: pathlib.Path, agent_name: str):
    atexit.register(remove_agent_dir, agent_name, path)
    create_agent_class(agent_name, path, True)
    edit_project_config_file(agent_name, path)
    atexit.unregister(remove_agent_dir)
