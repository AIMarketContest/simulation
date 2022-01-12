import pathlib
import shutil

from ai_market_contest.cli.utils.filesystemutils import (  # type: ignore
    assert_proj_dir_exists,
)


def remove_proj_dir(proj_dir: pathlib.Path):
    assert_proj_dir_exists(proj_dir)
    shutil.rmtree(proj_dir)
