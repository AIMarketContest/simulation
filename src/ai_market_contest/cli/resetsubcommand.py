import pathlib
import shutil
import sys
from cli_config import PROJ_DIR_NAME


def remove_proj_dir(path_exists, proj_dir):
    if not path_exists:
        print("Illegal argument: Argument must be an existing directory")
        sys.exit(2)
    if not proj_dir.is_dir():
        print("Illegal argument: No agent has been initialised at this directory")
        sys.exit(2)
    shutil.rmtree(proj_dir)


def reset_file_structure(args):
    path = args.path
    proj_dir: pathlib.Path = path / PROJ_DIR_NAME
    remove_proj_dir(path.is_dir(), proj_dir)


def create_subparser(subparsers):
    parser_reset = subparsers.add_parser(
        "reset", help="Reset the initialised folder structure for the project"
    )
    parser_reset.add_argument("path", type=pathlib.Path, default=".")
    parser_reset.set_defaults(func=reset_file_structure)
