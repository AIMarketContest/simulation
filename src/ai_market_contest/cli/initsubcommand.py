import os
import pathlib
import shutil
import sys
import atexit


def make_agent_classname_camelcase(agent_name):
    AGENT_STR = "agent"
    agent_name_cc = agent_name.lower()
    if AGENT_STR in agent_name_cc:
        agent_name_cc = agent_name_cc.replace(AGENT_STR, AGENT_STR.capitalize())
    return agent_name_cc[0].upper() + agent_name_cc[1:]


def make_agent_class(proj_dir: pathlib.Path, agent_name: str):
    IMPORT_STR = "import"
    AGENT_STR = "Agent"
    ABS_METHOD_STR = "abstractmethod"
    CLASS_METHOD_STR = "classmethod"
    agent_filename: str = agent_name + ".py"
    agent_file: pathlib.Path = proj_dir / agent_filename
    agent_file.touch()
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
                        f1.write(
                            "class "
                            + make_agent_classname_camelcase(agent_name)
                            + "(Agent):\n"
                        )
                    else:
                        f1.write(line)
        f2.close()
    f1.close()


def make_proj_dir(path_exists, proj_dir):
    if not path_exists:
        raise IllegalArgumentError
    if proj_dir.is_dir():
        print(
            "Agent already initialised\nIf you want to delete the current agent and start a new one,\nedit the agent.ini file\nthen run the command ai-market-contest restart <path>"
        )
        sys.exit(2)
    os.mkdir(proj_dir)


def initialise_file_structure(path):
    proj_dir = path / "aicontest"
    make_proj_dir(path.is_dir(), proj_dir)
    print("Enter name of the agent ", end="")
    agent_name = input()
    print("Enter name(s) of the author(s): ", end="")
    authors = input().split(",")
    make_agent_class(proj_dir, agent_name)


def create_subparser(subparsers):
    parser_init = subparsers.add_parser(
        "init",
        help="Initialises a folder structure for a project",
    )
    parser_init.add_argument("path", type=pathlib.Path, default="."),
    parser_init.set_defaults(func=initialise_file_structure)
