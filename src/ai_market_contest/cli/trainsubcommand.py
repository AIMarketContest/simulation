import pathlib
import sys
from typing import Any

from ai_market_contest.cli.cli_config import (
    PROJ_DIR_NAME,
    AGENTS_DIR_NAME,
    TRAINED_AGENTS_DIR_NAME,
    COMMAND_NAME,
    PICKLE_FILENAME,
)
from ai_market_contest.cli.utils.hashing import (
    get_shortened_hashes,
    get_agent_initial_hash,
)
from ai_market_contest.cli.utils.filesystemutils import (  # type: ignore
    check_path_exists,
    check_directory_exists,
    check_proj_dir_exists,
)
from ai_market_contest.cli.utils.getagents import (  # type: ignore
    get_agent_names,
    get_trained_agents,
)
from ai_market_contest.cli.utils.displayagents import (  # type: ignore
    display_agents,
    display_trained_agents,
)

from ai_market_contest.cli.utils.checkagentinitialisation import (
    check_agent_is_initialised,
)
from ai_market_contest.cli.utils.training import train


def ask_for_trained_agents(agent: str) -> bool:
    max_count = 3
    count = 0
    while count < max_count:
        char = input("Would you like to train a trained version of the agent (y/n): ")
        if char == "n" or char == "y":
            return True if char == "y" else False
    print("Operation aborted: failed to get valid input")
    sys.exit(1)


def choose_agent_for_training(agent_names: list[str]) -> str:
    print("Choose an agent to train: ", end="")
    while True:
        chosen_agent = input()
        if chosen_agent in agent_names:
            break
        print(f"{chosen_agent} not an existing agent")
        print("Choose a valid agent to train: ")
    return chosen_agent


def choose_trained_agent(trained_agents: list[str]):
    shortened_hashes = get_shortened_hashes(trained_agents)
    max_count = 3
    count = 0
    print(
        "\nInput the hash or index of the version of the agent to be trained: ", end=""
    )
    while count < max_count:
        count += 1
        trained_agent = input()
        if trained_agent in trained_agents or trained_agent in shortened_hashes:
            break
        if trained_agent.isnumeric():
            if int(trained_agent) in range(len(trained_agents)):
                index = int(trained_agent)
                trained_agent = trained_agents[index]
                break
        print(
            f"Hash or index {trained_agent} does not correspond to an existing version of the agent"
        )
        print(
            "Enter a valid hash or index of the version of the agent to be trained: ",
            end="",
        )
    if count >= max_count:
        print("\nOperation Aborted: Invalid hash or index")
        sys.exit(1)
    return trained_agent


def train_agent(args: Any):
    path: pathlib.Path = args.path
    proj_dir: pathlib.Path = path / PROJ_DIR_NAME
    check_path_exists(path)
    check_proj_dir_exists(proj_dir)
    agent_names: list[str] = get_agent_names(proj_dir)
    display_agents(agent_names)
    chosen_agent: str = choose_agent_for_training(agent_names)
    agents_dir: pathlib.Path = proj_dir / AGENTS_DIR_NAME
    chosen_agent_dir: pathlib.Path = agents_dir / chosen_agent
    error_msg: str = f"Error: no directory exists for {chosen_agent}"
    check_directory_exists(chosen_agent_dir, error_msg)
    agent_is_initialised = check_agent_is_initialised(chosen_agent_dir)
    if not agent_is_initialised:
        print(
            "Agent must be initialised before training. To initialise the agent, "
            + "edit the initial_pickler.py file in the agent folder, then run"
        )
        print(f"{COMMAND_NAME} initialise-agent <path>")
        print("and pick the agent you want to initialise")
        sys.exit(0)
    chosen_trained_agent: str = get_agent_initial_hash(chosen_agent_dir)
    show_trained_agents: bool = ask_for_trained_agents(chosen_agent)
    if show_trained_agents:
        trained_agents: list[str] = get_trained_agents(chosen_agent_dir)
        display_trained_agents(chosen_agent_dir, trained_agents)
        chosen_trained_agent = choose_trained_agent(trained_agents)
    training_agent_dir = (
        chosen_agent_dir / TRAINED_AGENTS_DIR_NAME / chosen_trained_agent
    )
    error_msg: str = f"Error: no directory exists for {chosen_trained_agent}"
    check_directory_exists(training_agent_dir, error_msg)
    training_msg: str = input("(Optional) Enter training message: ")
    training_agent_pkl_file = training_agent_dir / PICKLE_FILENAME
    train(chosen_agent_dir, chosen_trained_agent, training_msg, training_agent_pkl_file)


def create_subparser(subparsers: Any):  # type: ignore
    parser_train = subparsers.add_parser(
        "train", help="Train an agent within a specified environment"
    )
    parser_train.add_argument("path", type=pathlib.Path, default=".")
    parser_train.set_defaults(func=train_agent)
