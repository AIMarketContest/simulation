import os
import pathlib
import shutil


def initialise_file_structure(path):
    if not path.is_dir():
        raise IllegalArgumentError
    os.mkdir(path / "aicontest")
    shutil.copyfile("../agent.py", path / "aicontest" / "agent.py")


def create_subparser(subparsers):
    parser_init = subparsers.add_parser(
        "init",
        help="Initialises a folder structure for a project",
    )
    parser_init.add_argument("path", type=pathlib.Path, default="."),
    parser_init.set_defaults(func=initialise_file_structure)
