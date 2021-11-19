import pathlib
import shutil
import sys
from typing import Any

from ai_market_contest.cli.cli_config import PROJ_DIR_NAME  # type: ignore
from ai_market_contest.cli.utils import check_path_exists, check_proj_dir_exists  # type: ignore


def remove_proj_dir(path_exists: bool, proj_dir: pathlib.Path):
    check_path_exists(path_exists)
    check_proj_dir_exists(proj_dir)
    shutil.rmtree(proj_dir)


def reset_file_structure(args: Any):
    path = args.path
    proj_dir: pathlib.Path = path / PROJ_DIR_NAME
    remove_proj_dir(path.is_dir(), proj_dir)


def create_subparser(subparsers: Any):  # type: ignore
    parser_reset = subparsers.add_parser(
        "reset", help="Reset the initialised folder structure for the project"
    )
    parser_reset.add_argument("path", type=pathlib.Path, default=".")
    parser_reset.set_defaults(func=reset_file_structure)
