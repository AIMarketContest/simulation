import pathlib


def get_checkpoint_path(dir_path: pathlib.Path):
    return str((dir_path / "checkpoint_000001/checkpoint-1").resolve())
