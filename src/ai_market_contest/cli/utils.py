import ast
import configparser
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
)

def display_agents(agents: list[str]):
    print("The current initialised agents are: ")
    print(f"[{', '.join(agents)}]")

def get_trained_agents(agent_dir: pathlib.Path): -> list[str]
    agent_config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    check_config_file_exists(agent_config_file)    config.read(agent_config_file)
    try:
        trained_agents: list[str] = ast.literal_eval(config["training"]["trained-agents"])
    except KeyError:
        print("Error: Config file needs a trained-agents attribute")
        sys.exit(1)
    return trained_agents

def check_config_file_exists(config_file: pathlib.Path):
    if not config_file.is_dir():
        print("Error: config file not found")
        sys.exit(2)


def get_agent_names(proj_dir: pathlib.Path): -> list[str]
    config: configparser.ConfigParser() = configparser.ConfigParser()
    config_file: pathlib.Path = proj_dir / CONFIG_FILENAME
    check_config_file_exists(config_file)
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
    config["training"]["trained-agents"] = "[]"
    with agent_config_file.open("w") as f:
        config.write(f)
