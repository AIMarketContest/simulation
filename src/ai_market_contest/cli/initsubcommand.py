import atexit
import configparser
import pathlib
import shutil
import sys
from typing import Any, List

from cli_config import (
    AGENT_FILE,
    CONFIG_FILENAME,
    EXAMPLE_MAIN_FILE,
    EXAMPLE_MAIN_FILENAME,
    PROJ_DIR_NAME,
    AGENTS_DIR_NAME,
)

from utils import write_to_new_agent_file, write_agent_config_file, input_agent_name


def make_agents_classes(proj_dir: pathlib.Path, agents_names: list[str]):
    agents_dir: pathlib.Path = proj_dir / AGENTS_DIR_NAME
    for agent_name in agents_names:
        agent_filename: str = agent_name + ".py"
        agent_dir = agents_dir / agent_name
        agent_dir.mkdir(parents=True)
        agent_file: pathlib.Path = agent_dir / agent_filename
        agent_file.touch()
        agent_config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
        write_to_new_agent_file(agent_file, agent_name)
        write_agent_config_file(agent_config_file)


def make_proj_dir(proj_dir: pathlib.Path):
    if proj_dir.is_dir():
        print(
            """Agent already initialised
            To delete the current agent and start a new one,
            edit the agent.ini file
            then run the command ai-market-contest restart <path>
            To just delete the current agent run ai-market-contest reset <path>"""
        )
        sys.exit(2)
    agents_dir: pathlib.Path = proj_dir / AGENTS_DIR_NAME
    agents_dir.mkdir(parents=True)


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


def include_example(proj_dir: pathlib.Path):
    shutil.copy(EXAMPLE_MAIN_FILE, proj_dir / EXAMPLE_MAIN_FILENAME)
    print(
        "The example on how to setup the environment can be found in example_main.py."
    )


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
    if args.include_example:
        include_example(proj_dir)
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
    parser_init.add_argument(
        "--include-example",
        action="store_true",
        help="Includes an example showing how to setup the environment",
    )
    parser_init.set_defaults(func=initialise_file_structure)
