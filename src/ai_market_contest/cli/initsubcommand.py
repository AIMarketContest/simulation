import os
import pathlib
import shutil
import sys
import atexit
import configparser
from cli_config import PROJ_DIR_NAME


def make_agent_classname_camelcase(agent_name):
    AGENT_STR = "agent"
    agent_name_cc = agent_name.lower()
    if AGENT_STR in agent_name_cc:
        agent_name_cc = agent_name_cc.replace(AGENT_STR, AGENT_STR.capitalize())
    return agent_name_cc[0].upper() + agent_name_cc[1:]


def make_agents_classes(proj_dir: pathlib.Path, agents_names: list[str]):
    IMPORT_STR: str = "import"
    AGENT_STR: str = "Agent"
    ABS_METHOD_STR: str = "abstractmethod"
    CLASS_METHOD_STR: str = "classmethod"
    for agent_name in agents_names:
        agent_filename: str = agent_name + ".py"
        agent_file: pathlib.Path = proj_dir / agent_filename
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


def make_proj_dir(path_exists, proj_dir):
    if not path_exists:
        print("Illegal argument: Argument must be an existing directort")
        sys.exit(2)
    if proj_dir.is_dir():
        print(
            "Agent already initialised\nTo delete the current agent and start a new one,\nedit the agent.ini file\nthen run the command ai-market-contest restart <path>\nTo just delete the current agent run ai-market-contest reset <path>"
        )
        sys.exit(2)
    os.mkdir(proj_dir)


def make_config_file(proj_dir, agents_names, authors):
    config: configparser.ConfigParser = configparser.ConfigParser()
    config["agent"] = {"agents": agents_names, "authors": authors}
    c_file: pathlib.Path = proj_dir / "config.ini"
    c_file.touch()
    with c_file.open("w") as config_file:
        config.write(config_file)


def remove_proj_dir(proj_dir):
    if proj_dir.is_dir():
        shutil.rmtree(proj_dir)


def include_example(proj_dir):
    shutil.copy("../example_main.py", proj_dir / "example_main.py")
    print(
        "The example on how to setup the environment can be found in example_main.py."
    )


def initialise_file_structure(args):
    path = args.path
    proj_dir = path / PROJ_DIR_NAME
    make_proj_dir(path.is_dir(), proj_dir)
    atexit.register(remove_proj_dir, proj_dir)
    agents_names: list[str] = []
    for agent_number in range(1, args.number_of_agents + 1):
        print(f"Enter name of agent {agent_number}: ", end="")
        agent_name: str = input()
        agents_names.append(agent_name)
    print("Enter name(s) of the author(s): ", end="")
    authors: list[str] = input().split(",")
    make_agents_classes(proj_dir, agents_names)
    make_config_file(proj_dir, agents_names, authors)
    if args.include_example:
        include_example(proj_dir)
    atexit.unregister(remove_proj_dir)


def create_subparser(subparsers):
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
