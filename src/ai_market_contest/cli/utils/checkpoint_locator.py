import pathlib

from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.filesystemutils import check_directory_exists


def get_checkpoint_path(
    dir_path: pathlib.Path,
    checkpoint_should_exist: bool,
    training_config_reader: TrainingConfigReader,
) -> str:
    epochs_str = str(training_config_reader.get_num_epochs())
    checkpoint_path: pathlib.Path = (
        dir_path / "checkpoint_"
        + "0" * (6 - len(epochs_str))
        + epochs_str / "checkpoint-"
        + str(epochs)
    ).resolve()
    if checkpoint_should_exist:
        error_msg: str = "No checkpoint exists at " + str(checkpoint_path)
        check_directory_exists(checkpoint_path, error_msg)
    return str(checkpoint_path)
