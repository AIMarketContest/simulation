import pathlib
import shutil

from ai_market_contest.cli.cli_config import PROJ_DIR_NAME  # type: ignore
from ai_market_contest.cli.utils.filesystemutils import (  # type: ignore
    check_path_exists,
    check_proj_dir_exists,
)


def remove_proj_dir(proj_dir: pathlib.Path):
    check_proj_dir_exists(proj_dir)
    shutil.rmtree(proj_dir)
