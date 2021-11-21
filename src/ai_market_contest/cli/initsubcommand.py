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
    EXAMPLE_MAIN_FILE,
    EXAMPLE_MAIN_FILENAME,
    PROJ_DIR_NAME,
)
from ai_market_contest.cli.utils.inputagentname import input_agent_name
from ai_market_contest.cli.utils.initialiseagent import (  # type: ignore
    create_new_agent_file,
    make_initial_trained_agent,
)
from ai_market_contest.cli.utils.hashing import set_agent_initial_hash


def make_agents_classes(proj_dir: pathlib.Path, agents_names: list[str]):
    agents_dir: pathlib.Path = proj_dir / AGENTS_DIR_NAME
    for agent_name in agents_names:
        agent_filename: str = agent_name + ".py"
        agent_dir = agents_dir / agent_name
        agent_dir.mkdir(parents=True)
        agent_file: pathlib.Path = agent_dir / agent_filename
        agent_file.touch()
        create_new_agent_file(agent_file, agent_name)
        initial_hash: str = set_agent_initial_hash(agent_dir)
        make_initial_trained_agent(agent_dir, initial_hash)


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
    agents_dir.mkdir(parents=True)
    environments_dir.mkdir()


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
