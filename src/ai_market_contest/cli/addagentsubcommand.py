import pathlib
import sys
import shutil
import configparser
import ast
from cli_config import PROJ_DIR_NAME, CONFIG_FILENAME
from initsubcommand import make_agent_classname_camelcase

def create_agent_class(agent_name, proj_dir):
    IMPORT_STR: str = "import"
    AGENT_STR: str = "Agent"
    ABS_METHOD_STR: str = "abstractmethod"
    CLASS_METHOD_STR: str = "classmethod"
    agent_filename: str = agent_name + ".py"
    agent_file: pathlib.Path = proj_dir / agent_filename
    if agent_file.is_file():
        overwrite = 'x'
        while overwrite != 'y' and overwrite != 'n':
            overwrite = input(f"{agent_filename} already exists, are you sure you want to override the existing file? (y/n): ")
            if overwrite == 'y':
                break
            if overwrite == 'n':
                sys.exit(0)
            
    agent_file.touch()
    class_line_tab = False
    with agent_file.open("w") as f1:
        f1.write("from agent import Agent\n")
        with open("../agent.py", "r") as f2:
            for line in f2:
                if line != None:
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
        f2.close()
    f1.close()


def add_agent(args):
    path = args.path
    if not path.is_dir():
        print("Illegal argument: Argument must be an existing directory")
        sys.exit(2)
    proj_dir = path / PROJ_DIR_NAME
    if not proj_dir.is_dir():
        print(
            "No project has been initialised in the directory.\nTo initialise a project run aicontest init <path>"
        )
        sys.exit(2)
    agent_name = input("Enter name of new agent: ")
    create_agent_class(agent_name, proj_dir)
    c_file = proj_dir / CONFIG_FILENAME
    config = configparser.ConfigParser()
    config.read(c_file)
    agents = ast.literal_eval(config["agent"]["agents"])
    if not agent_name in agents:
        agents.append(agent_name)
    config["agent"]["agents"] = str(agents)
    with c_file.open("w") as config_file:
        config.write(config_file)


def create_subparser(subparsers):
    parser_addagent = subparsers.add_parser(
        "add-agent", help="Adds an agent to an initialised project"
    )
    parser_addagent.add_argument("path", type=pathlib.Path, default=".")
    parser_addagent.set_defaults(func=add_agent)
