import pathlib

from ai_market_contest.cli.utils.filesystemutils import check_directory_exists


def get_checkpoint_path(dir_path: pathlib.Path, checkpoint_should_exist: bool) -> str:
    checkpoint_path: pathlib.Path = (
        dir_path / "checkpoint_000001/checkpoint-1"
    ).resolve()
    if checkpoint_should_exist:
        error_msg: str = "No checkpoint exists at " + str(checkpoint_path)
        check_directory_exists(checkpoint_path, error_msg)
    return str(checkpoint_path)
