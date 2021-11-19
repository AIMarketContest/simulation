import pathlib
from typing import Any

from ai_market_contest.cli.cli_config import PROJ_DIR_NAME
from ai_market_contest.cli.utils import (
    check_path_exists,
    check_proj_dir_exists,
    get_agent_names,
    display_agents,
    choose_agent_for_training,
    ask_for_trained_agents,
    display_trained_agents,
    get_trained_agents,
    check_directory_exists,
    choose_trained_agent,
)  # type: ignore


def train_agent(args: Any):
    path: pathlib.Path = args.path
    proj_dir = path / PROJ_DIR_NAME
    check_path_exists(path.is_dir())
    check_proj_dir_exists(proj_dir)
    agent_names: list[str] = get_agent_names(proj_dir)
    display_agents(agent_names)
    chosen_agent: str = choose_agent_for_training(agent_names)
    show_trained_agents = ask_for_trained_agents(chosen_agent)
    agents_dir: pathlib.Path = proj_dir / AGENTS_DIR_NAME
    chosen_agent_dir: pathlib.Path = agents_dir / chosen_agent
    error_msg = f"Error: no directory exists for {chosen_agent}"
    check_directory_exists(chosen_agent_dir, error_msg)
    if get_trained_agents:
        trained_agents = get_trained_agents(chosen_agent_dir)
        display_trained_agents()
        chosen_trained_agent = choose_trained_agent(trained_agents)


def create_subparser(subparsers: Any):  # type: ignore
    parser_train = subparsers.add_parser(
        "train", help="Train an agent within a specified environment"
    )
    parser_train.add_argument("path", type=pathlib.Path, default=".")
    parser_train.set_defaults(func=train_agent)
