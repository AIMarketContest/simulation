import pathlib
import sys

from ai_market_contest.cli.cli_config import COMMAND_NAME


def check_directory_exists(directory: pathlib.Path, error_msg: str):
    if not directory.is_dir():
        print(error_msg)
        sys.exit(2)


def check_file_exists(file_path: pathlib.Path, error_msg: str):
    if not file_path.is_file():
        print(error_msg)
        sys.exit(2)


def check_proj_dir_exists(proj_dir: pathlib.Path):
    error_msg: str = (
        "Illegal argument: No project has been initialised at this directory"
        + f"To initialise a new project run {COMMAND_NAME} init <path>"
    )
    check_directory_exists(proj_dir, error_msg)


def check_path_exists(path: pathlib.Path):
    error_msg: str = "Illegal argument: Argument must be an existing directory"
    check_directory_exists(path, error_msg)


def check_config_file_exists(config_file: pathlib.Path):
    error_msg: str = "Error: config file does not exist"
    check_file_exists(config_file, error_msg)