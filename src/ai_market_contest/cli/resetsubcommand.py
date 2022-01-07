import pathlib
import shutil
from typing import Any

from ai_market_contest.cli.cli_config import PROJ_DIR_NAME  # type: ignore
from ai_market_contest.cli.utils.filesystemutils import (  # type: ignore
    check_path_exists,
    check_proj_dir_exists,
)


def remove_proj_dir(path: pathlib.Path, proj_dir: pathlib.Path):
    check_path_exists(path)
    check_proj_dir_exists(proj_dir)
    shutil.rmtree(proj_dir)


def reset_file_structure(args: Any):
    path = args.path
    proj_dir: pathlib.Path = path / PROJ_DIR_NAME
    remove_proj_dir(path, proj_dir)