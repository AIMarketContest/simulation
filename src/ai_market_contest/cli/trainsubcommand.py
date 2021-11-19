import pathlib
from typing import Any

from ai_market_contest.cli.cli_config import PROJ_DIR_NAME
from ai_market_contest.cli.utils import check_path_exists, check_proj_dir_exists  # type: ignore


def train_agent(args: Any):
    path: pathlib.Path = args.path
    proj_dir = path / PROJ_DIR_NAME
    check_path_exists(path_exists)
    check_proj_dir_exists(proj_dir)


def create_subparser(subparsers: Any):  # type: ignore
    parser_train = subparsers.add_parser(
        "train", help="Train an agent within a specified environment"
    )
    parser_train.add_argument("path", type=pathlib.Path, default=".")
    parser_train.set_defaults(func=train_agent)
