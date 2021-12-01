import atexit
import configparser
import pathlib
import shutil
import sys
from typing import Any, List

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    COMMAND_NAME,
    CONFIG_FILENAME,
    ENVS_DIR_NAME,
    PROJ_DIR_NAME,
    TRAINING_CONFIGS_DIR_NAME,
)
from ai_market_contest.cli.utils.hashing import set_agent_initial_hash
from ai_market_contest.cli.utils.initialiseagent import create_agent_class
from ai_market_contest.cli.utils.inputagentname import input_agent_name


def make_agents_classes(proj_dir: pathlib.Path, agents_names: list[str]):
    agents_dir: pathlib.Path = proj_dir / AGENTS_DIR_NAME
    for agent_name in agents_names:
        create_agent_class(agent_name, proj_dir)


def make_proj_dir(proj_dir: pathlib.Path):
    if proj_dir.is_dir():
        print(
            f"""{PROJ_DIR_NAME} project already initialised in the given directory 
            To delete the current project run {COMMAND_NAME} reset <path> 
            To add an agent to the project run {COMMAND_NAME} add-agent <path>"""
        )
        sys.exit(2)
    agents_dir: pathlib.Path = proj_dir / AGENTS_DIR_NAME
    environments_dir: pathlib.Path = proj_dir / ENVS_DIR_NAME
    training_configs_dir: pathlib.Path = proj_dir / TRAINING_CONFIGS_DIR_NAME
    agents_dir.mkdir(parents=True)
    environments_dir.mkdir(parents=True)
    training_configs_dir.mkdir(parents=True)


def make_config_file(
    proj_dir: pathlib.Path, agents_names: List[str], authors: List[str]
):
    config: configparser.ConfigParser = configparser.ConfigParser()
    config["agent"] = {"agents": agents_names, "authors": authors}  # type: ignore
    c_file: pathlib.Path = proj_dir / CONFIG_FILENAME
    c_file.touch()
    with c_file.open("w") as config_file:
        config.write(config_file)


def remove_proj_dir(proj_dir: pathlib.Path):
    if proj_dir.is_dir():
        shutil.rmtree(proj_dir)


def initialise_file_structure(args: Any):
    path: pathlib.Path = args.path
    proj_dir = path / PROJ_DIR_NAME
    make_proj_dir(proj_dir)
    atexit.register(remove_proj_dir, proj_dir)
    agents_names: list[str] = []
    for agent_number in range(1, args.number_of_agents + 1):
        print(f"Enter name of agent {agent_number}: ", end="")
        agent_name = input_agent_name(agents_names)
        agents_names.append(agent_name)
    print("Enter name(s) of the author(s): ", end="")
    authors: list[str] = input().split(",")
    make_agents_classes(proj_dir, agents_names)
    make_config_file(proj_dir, agents_names, authors)
    atexit.unregister(remove_proj_dir)


def create_subparser(subparsers: Any):  # type: ignore
    parser_init = subparsers.add_parser(
        "init",
        help="Initialises a folder structure for a project",
    )
    parser_init.add_argument("path", type=pathlib.Path, default=".")
    parser_init.add_argument(
        "-n",
        metavar="number_of_agents",
        type=int,
        help="Number of agent templates to make",
        default=1,
        dest="number_of_agents",
    )

    parser_init.set_defaults(func=initialise_file_structure)
