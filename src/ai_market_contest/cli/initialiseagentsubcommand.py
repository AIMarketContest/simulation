import pathlib
from typing import Any

from ai_market_contest.cli.cli_config import PROJ_DIR_NAME, AGENTS_DIR_NAME
from ai_market_contest.cli.utils.filesystemutils import (  # type: ignore
    check_path_exists,
    check_proj_dir_exists,
    check_directory_exists,
)
from ai_market_contest.cli.utils.getagents import get_agent_names
from ai_market_contest.cli.utils.displayagents import display_agents
from ai_market_contest.cli.utils.pklfileutils import initialise_agent_pkl_file
from ai_market_contest.cli.utils.initialiseagent import set_agent_to_initialised


def choose_agent_for_initialising(agent_names: list[str]) -> str:
    print("Choose an agent to initialise: ", end="")
    while True:
        chosen_agent = input()
        if chosen_agent in agent_names:
            break
        print(f"{chosen_agent} not an existing agent")
        print("Choose a valid agent to train: ")
    return chosen_agent


def initialise_agent(args: Any):
    path: pathlib.Path = args.path
    proj_dir: pathlib.Path = path / PROJ_DIR_NAME
    check_path_exists(path)
    check_proj_dir_exists(proj_dir)
    agent_names: list[str] = get_agent_names(proj_dir)
    display_agents(agent_names)
    chosen_agent: str = choose_agent_for_initialising(agent_names)
    agents_dir: pathlib.Path = proj_dir / AGENTS_DIR_NAME
    chosen_agent_dir: pathlib.Path = agents_dir / chosen_agent
    error_msg: str = f"Error: no directory exists for {chosen_agent}"
    check_directory_exists(chosen_agent_dir, error_msg)
    initialise_agent_pkl_file(chosen_agent_dir)
    set_agent_to_initialised(chosen_agent_dir)
    print("Agent successfully initialised")


def create_subparser(subparsers: Any):  # type: ignore
    parser_train = subparsers.add_parser(
        "initialise-agent", help="Initialise an agent for training"
    )
    parser_train.add_argument("path", type=pathlib.Path, default=".")
    parser_train.set_defaults(func=initialise_agent)
