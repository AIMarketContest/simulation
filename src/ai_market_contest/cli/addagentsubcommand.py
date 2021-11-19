import ast
import configparser
import pathlib
import sys
from typing import Any

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENT_FILE,
    CONFIG_FILENAME,
    PROJ_DIR_NAME,
)
from ai_market_contest.cli.utils import write_to_new_agent_file  # type: ignore


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
    create_agent_class(agent_name, proj_dir)
    c_file = proj_dir / CONFIG_FILENAME
    config = configparser.ConfigParser()
    config.read(c_file)
    agents = ast.literal_eval(config["agent"]["agents"])
    if agent_name not in agents:
        agents.append(agent_name)
    config["agent"]["agents"] = str(agents)
    with c_file.open("w") as config_file:
        config.write(config_file)


def create_subparser(subparsers: Any):  # type: ignore
    parser_addagent = subparsers.add_parser(
        "add-agent", help="Adds an agent to an initialised project"
    )
    parser_addagent.add_argument("path", type=pathlib.Path, default=".")
    parser_addagent.set_defaults(func=add_agent)
