import ast
import atexit
import configparser
import pathlib
import sys
from typing import Any

from cli_config import AGENT_FILE, CONFIG_FILENAME, PROJ_DIR_NAME
from utils import (
    write_to_new_agent_file,
    write_agent_config_file,
)


def create_agent_class(agent_name: str, proj_dir: pathlib.Path):
    agent_filename: str = agent_name + ".py"
    agent_dir: pathlib.Path = proj_dir / agent_name
    agent_file: pathlib.Path = agent_dir / agent_filename
    if agent_dir.is_dir():
        overwrite = "x"
        while overwrite != "y" and overwrite != "n":
            overwrite = input(
                f"{agent_filename} already exists, are you sure you want"
                + " to override the existing file? (y/n): "
            )
            if overwrite == "y":
                break
            if overwrite == "n":
                sys.exit(0)
    agent_dir.mkdir(parents=True)
    agent_file.touch()
    write_to_new_agent_file(agent_file, agent_name)
    agent_config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    write_agent_config_file(agent_config_file)


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
    agent_dir = proj_dir / agent_name
    if agent_dir.is_dir():
        shutil.rmtree(agent_dir)
    config_file: pathlib.Path = proj_dir / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    agents: list[str] = ast.lteral_eval(config["agent"]["agents"])
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
    agent_name = input("Enter name of new agent: ")
    atexit.register(remove_agent_dir, agent_name, proj_dir)
    create_agent_class(agent_name, proj_dir)
    edit_project_config_file(agent_name, proj_dir)
    atexit.unregister(remove_agent_dir)


def create_subparser(subparsers: Any):  # type: ignore
    parser_addagent = subparsers.add_parser(
        "add-agent", help="Adds an agent to an initialised project"
    )
    parser_addagent.add_argument("path", type=pathlib.Path, default=".")
    parser_addagent.set_defaults(func=add_agent)
