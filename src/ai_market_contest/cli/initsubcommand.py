import os
import pathlib
import shutil
import sys


def make_agent_class(proj_dir, agent_name):
    agent_filename = agent_name + ".py"
    agent_file = proj_dir / agent_filename
    agent_file.touch()
    with agent_file.open("a") as f1:
        with open("../agent.py", "r") as f2:
            f1.writelines(f2.readlines())


def initialise_file_structure(path):
    proj_dir = path / "aicontest"
    if not path.is_dir():
        raise IllegalArgumentError
    if proj_dir.is_dir():
        print(
            "Agent already initialised\nIf you want to delete the current agent and start a new one,\nedit the agent.ini file\nthen run the command ai-market-contest restart <path>"
        )
        sys.exit(2)
    print("Enter name of the agent ", end="")
    agent_name = input()
    print("Enter name(s) of the author(s): ", end="")
    authors = input().split(",")
    os.mkdir(proj_dir)
    make_agent_class(proj_dir, agent_name)


def create_subparser(subparsers):
    parser_init = subparsers.add_parser(
        "init",
        help="Initialises a folder structure for a project",
    )
    parser_init.add_argument("path", type=pathlib.Path, default="."),
    parser_init.set_defaults(func=initialise_file_structure)
