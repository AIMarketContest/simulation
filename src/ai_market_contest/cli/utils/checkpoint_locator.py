import pathlib
from typing import Final

from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.filesystemutils import check_file_exists


def get_checkpoint_path(
    dir_path: pathlib.Path,
    checkpoint_should_exist: bool,
    training_config_reader: TrainingConfigReader,
) -> str:
    NUM_CHECKPOINT_DIGITS: Final = 6
    epochs_str: str = str(training_config_reader.get_num_epochs())
    checkpoint_path: pathlib.Path = (
        dir_path
        / (
            f"checkpoint_{'0'*(NUM_CHECKPOINT_DIGITS - len(epochs_str))}"
            + f"{epochs_str}/checkpoint-{epochs_str}"
        )
    ).resolve()
    if checkpoint_should_exist:
        error_msg: str = f"No checkpoint exists at {str(checkpoint_path)}"
        check_file_exists(checkpoint_path, error_msg)
    return str(checkpoint_path)
