import ast
import configparser
import datetime
import pathlib
import sys
from hashlib import sha1 as hashing_algorithm

from ai_market_contest.cli.cli_config import (  # type: ignore
    ABS_METHOD_STR,
    AGENT_FILE,
    AGENT_STR,
    CLASS_METHOD_STR,
    CONFIG_FILENAME,
    IMPORT_STR,
    PROJ_DIR_NAME,
    COMMAND_NAME,
    META_FILENAME,
    TRAINED_AGENTS_DIR_NAME,
    HASH_LENGTH,
)


def check_directory_exists(directory: pathlib.Path, error_msg: str):
    if not directory.is_dir():
        print(error_msg)
        sys.exit(2)


def check_file_exists(file_path: pathlib.Path, error_msg: str):
    if not file_path.is_file():
        print(error_msg)
        sys.exit(2)


def get_agent_initial_hash(chosen_agent_dir: pathlib.Path):
    agent_config_file: pathlib.Path = chosen_agent_dir / CONFIG_FILENAME
    check_config_file_exists(agent_config_file)
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(agent_config_file)
    try:
        initial_hash = ast.literal_eval(config["training"]["initial-hash"])
    except KeyError:
        print("Error: agent config missing an initial hash")
        sys.exit(1)
    return initial_hash


def get_trained_agent_metadata(agent_dir: pathlib.Path, trained_agent_name: str):
    trained_agents_dir: pathlib.Path = agent_dir / TRAINED_AGENTS_DIR_NAME
    trained_agent_dir: pathlib.Path = trained_agents_dir / trained_agent_name
    error_msg: str = f"Error: no folder exists for {trained_agent_name}"
    check_directory_exists(trained_agent_dir, error_msg)
    meta_file: pathlib.Path = trained_agent_dir / META_FILENAME
    error_msg: str = f"Error: no meta file exists for {trained_agent_name}"
    check_file_exists(meta_file, error_msg)
    return read_meta_file(meta_file)


def choose_trained_agent(trained_agents: list[str]):
    max_count = 3
    count = 0
    print("Input the hash of the version of the agent to be trained: ", end="")
    while count < max_count:
        count += 1
        trained_agent = input()
        if trained_agent in trained_agents:
            break
        print(
            f"Hash {trained_agent} does not correspond to an existing version of the agent"
        )
        print("Enter a valid hash of the version of the agent to be trained: ", end="")


def display_trained_agents(agent_dir: pathlib.Path, trained_agents: list[str]):
    for trained_agent in trained_agents:
        (agent_hash, time) = get_trained_agent_metadata(agent_dir, trained_agent)
        shortened_hash: str = agent_hash[:HASH_LENGTH]
        print(f"{shortened_hash} {str(time)}")


def ask_for_trained_agents(agent: str) -> bool:
    max_count = 3
    count = 0
    while count < max_count:
        char = input("Would you like to train a trained version of the agent (y/n): ")
        if char == "n" or char == "y":
            return True if char == "y" else False
    print("Operation aborted: failed to get valid input")
    sys.exit(1)


def read_meta_file(meta_file: pathlib.Path) -> (str, datetime.datetime):
    config: configparser.ConfigParser = configparser.ConfigParser()
    try:
        year = int(config["time"]["year"])
        month = int(config["time"]["month"])
        day = int(config["time"]["day"])
        hour = int(config["time"]["hour"])
        minute = int(config["time"]["minute"])
        second = int(config["time"]["second"])
    except KeyError:
        print("Error: Meta file missing time data")
        sys.exit(1)
    except ValueError:
        print("Error: time attribute must only contain numbers")
        sys.exit(1)
    try:
        time = datetime.datetime(year, month, day, hour, minute, second)
    except ValueError:
        print("Error: date time in meta file represents an invalid datetime")
        sys.exit(1)
    try:
        trained_agent_hash = config["trained-agent"]["hash"]
    except KeyError:
        print("Error: Meta file missing the trained agent hash")
        sys.exit(1)
    return (trained_agent_hash, time)


def write_meta_file(
    path: pathlib.Path, trained_agent_hash: str, time: datetime.datetime
):
    meta_file: pathlib.Path = path / META_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    config["time"] = {
        "year": time.year,
        "month": time.month,
        "day": time.day,
        "hour": time.hour,
        "minute": time.minute,
        "second": time.second,
    }
    config["trained-agent"] = {"hash": trained_agent_hash}

    with meta_file.open("w") as m_file:
        config.write(m_file)


def choose_agent_for_training(agent_names: list[str]) -> str:
    print("Choose an agent to train: ", end="")
    while True:
        chosen_agent = input()
        if chosen_agent in agent_names:
            break
        print(f"{chosen_agent} not an existing agent")
        print("Choose a valid agent to train: ")
    return chosen_agent


def display_agents(agents: list[str]):
    print("The current initialised agents are: ")
    print(f"[{', '.join(agents)}]")


def get_trained_agents(agent_dir: pathlib.Path) -> list[str]:
    agent_config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    check_config_file_exists(agent_config_file)
    config.read(agent_config_file)
    try:
        trained_agents: list[str] = ast.literal_eval(
            config["training"]["trained-agents"]
        )
    except KeyError:
        print("Error: Config file needs a trained-agents attribute")
        sys.exit(1)
    return trained_agents


def check_config_file_exists(config_file: pathlib.Path):
    if not config_file.is_file():
        print("Error: config file not found")
        sys.exit(2)


def get_agent_names(proj_dir: pathlib.Path) -> list[str]:
    config: configparser.ConfigParser() = configparser.ConfigParser()
    config_file: pathlib.Path = proj_dir / CONFIG_FILENAME
    check_config_file_exists(config_file)
    print("hi")
    config.read(config_file)
    try:
        agents: list[str] = ast.literal_eval(config["agent"]["agents"])
    except KeyError:
        print("Error: config file needs an agents attribute")
        sys.exit(1)
    return agents


def hash_string(string: str):
    return hashing_algorithm(string.encode()).hexdigest()


def check_path_exists(path_exists: bool):
    if not path_exists:
        print("Illegal argument: Argument must be an existing directory")
        sys.exit(2)


def check_proj_dir_exists(proj_dir: pathlib.Path):
    if not proj_dir.is_dir():
        print(
            "Illegal argument: No project has been initialised at this directory\n"
            + "To initialise a new project run "
            + COMMAND_NAME
            + " init <path>"
        )
        sys.exit(2)


def remove_underscores(string: str):
    return string.replace("_", "")


def is_valid_agent_name(agent_name: str):
    return agent_name[0].isalpha() and remove_underscores(agent_name).isalnum()


def input_agent_name(agents_names):
    while True:
        agent_name: str = input()
        if is_valid_agent_name(agent_name):
            if agent_name in agents_names:
                print("Two agents cannot have the same name")
                print("Please enter a valid agent name: ", end="")
                continue
            break
        print(
            "Agent name must begin with a letter and can only contain letters, numbers and underscores"
        )
        print("Enter a valid agent name: ", end="")
    return agent_name


def make_agent_classname_camelcase(agent_name: str):
    AGENT_STR = "agent"
    if AGENT_STR.capitalize() in agent_name:
        return agent_name
    agent_name_cc = agent_name.lower()
    if AGENT_STR in agent_name_cc:
        agent_name_cc = agent_name_cc.replace(AGENT_STR, AGENT_STR.capitalize())
    return agent_name_cc[0].upper() + agent_name_cc[1:]


def write_to_new_agent_file(agent_file: pathlib.Path, agent_name: str):
    class_line_tab: bool = False
    with agent_file.open("w") as f1:
        f1.write("from agent import Agent\n")
        with AGENT_FILE.open("r") as f2:
            for line in f2:
                if line is not None:
                    if CLASS_METHOD_STR in line:
                        break
                    if IMPORT_STR in line:
                        continue
                    if ABS_METHOD_STR in line:
                        continue
                    if AGENT_STR in line:
                        tab = "\t" if class_line_tab else ""
                        f1.write(
                            tab
                            + "class "
                            + make_agent_classname_camelcase(agent_name)
                            + "(Agent):\n"
                        )
                        class_line_tab = True
                    else:
                        f1.write(line)


def write_agent_config_file(agent_config_file: pathlib.Path):
    config: configparser.ConfigParser = configparser.ConfigParser()
    config["training"] = {"trained-agents": []}
    with agent_config_file.open("w") as f:
        config.write(f)
