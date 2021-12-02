import ast
import atexit
import configparser
import pathlib
import shutil
import sys
from typing import Any

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    CONFIG_FILENAME,
    PROJ_DIR_NAME,
)
from ai_market_contest.cli.utils.initialiseagent import create_agent_class
from ai_market_contest.cli.utils.inputagentname import input_agent_name


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


def remove_agent_dir(agent_name, proj_dir):
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


def add_agent(args: Any):
    path: pathlib.Path = args.path
    if not path.is_dir():
        print("Illegal argument: Argument must be an existing directory")
        sys.exit(2)
    proj_dir = path / PROJ_DIR_NAME
    if not proj_dir.is_dir():
        print(
            """No project has been initialised in the directory.
            To initialise a project run aicontest init <path>"""
        )
        sys.exit(2)
    print("Enter name of new agent: ", end="")
    agent_name = input_agent_name([])
    atexit.register(remove_agent_dir, agent_name, proj_dir)
    create_agent_class(agent_name, proj_dir, True)
    edit_project_config_file(agent_name, proj_dir)
    atexit.unregister(remove_agent_dir)


def create_subparser(subparsers: Any):  # type: ignore
    parser_addagent = subparsers.add_parser(
        "add-agent", help="Adds an agent to an initialised project"
    )
    parser_addagent.add_argument("path", type=pathlib.Path, default=".")
    parser_addagent.set_defaults(func=add_agent)
