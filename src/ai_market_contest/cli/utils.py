import pathlib
import configparser

from cli_config import (
    AGENT_FILE,
    CONFIG_FILENAME,
    PROJ_DIR_NAME,
    CLASS_METHOD_STR,
    IMPORT_STR,
    ABS_METHOD_STR,
    AGENT_STR,
)


def remove_underscores(string: str):
    return string.replace("_", "")


def is_valid_agent_name(agent_name: str):
    return agent_name[0].isalpha() and remove_underscores(agent_name).isalnum()


def input_agent_name():
    while True:
        agent_name: str = input()
        if is_valid_agent_name(agent_name):
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
    with agent_config_file.open("w"):
        config.write(agent_config_file)
