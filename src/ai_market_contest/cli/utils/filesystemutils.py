import pathlib
import sys

import typer

from ai_market_contest.cli.cli_config import COMMAND_NAME
from ai_market_contest.cli.utils.error_codes import ErrorCodes


def assert_directory_exists(directory: pathlib.Path, error_msg: str):
    if not directory.is_dir():
        print(error_msg)
        sys.exit(ErrorCodes.DIRECTORY_DOES_NOT_EXIST)


def assert_file_exists(file_path: pathlib.Path, error_msg: str):
    if not file_path.is_file():
        print(error_msg)
        sys.exit(ErrorCodes.FILE_DOES_NOT_EXIST)


def assert_proj_dir_exists(proj_dir: pathlib.Path):
    error_msg: str = (
        "Illegal argument: No project has been initialised at this directory\n"
        + f"To initialise a new project run {COMMAND_NAME} init <path>"
    )
    assert_directory_exists(proj_dir, error_msg)


def assert_path_exists(path: pathlib.Path):
    error_msg: str = "Illegal argument: Argument must be an existing directory"
    assert_directory_exists(path, error_msg)


def assert_config_file_exists(config_file: pathlib.Path):
    error_msg: str = "Error: config file does not exist"
    assert_file_exists(config_file, error_msg)


def check_overwrite(filename: str, dir: pathlib.Path):
    if dir.is_dir():
        prompt = f"{filename} already exists, are you sure you want to override the existing file?"
        overwrite = typer.confirm(text=prompt, default=None)
        if not overwrite:
            return False
    return True  # If not a directory, then we can go ahead and overwrite anyway
