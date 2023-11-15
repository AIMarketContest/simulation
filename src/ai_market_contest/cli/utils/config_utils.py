import pathlib
import shutil
import sys
from configparser import ConfigParser
from pathlib import Path

from ai_market_contest.cli.cli_config import (
    CONFIG_FILE_EXTENSION,
    EVALUATION_CONFIG_EXTENSION,
    EVALUATION_CONFIGS_DIR_NAME,
    EXAMPLE_EVALUATION_CONFIG,
    EXAMPLE_EVALUATION_CONFIG_FILE_NAME,
    EXAMPLE_TRAINING_CONFIG,
    EXAMPLE_TRAINING_CONFIG_FILE_NAME,
    TRAINING_CONFIG_EXTENSION,
    TRAINING_CONFIGS_DIR_NAME,
)
from ai_market_contest.cli.utils.error_codes import ErrorCodes
from ai_market_contest.cli.utils.filesystemutils import assert_config_file_exists


def assert_configs_exist(training_configs: list[str]) -> None:
    if not training_configs:
        print(
            "Operation aborted: no training configs have been defined in training_configs"
        )
        sys.exit(ErrorCodes.NO_TRAINING_CONFIGS)


def get_configs(proj_dir: Path, config_directory_name: str) -> list[str]:
    configs_dir = proj_dir / config_directory_name
    configs = []
    for config_file in configs_dir.rglob(f"*{CONFIG_FILE_EXTENSION}"):
        configs.append(config_file.stem)
    return configs


def get_training_configs(proj_dir: Path) -> list[str]:
    return get_configs(proj_dir, TRAINING_CONFIGS_DIR_NAME)


def get_evaluation_configs(proj_dir: Path) -> list[str]:
    return get_configs(proj_dir, EVALUATION_CONFIGS_DIR_NAME)


def get_training_config_path(proj_dir: Path, training_config: str) -> Path:
    # Add extension as was removed when displaying to users
    training_config_path: Path = (
        proj_dir
        / TRAINING_CONFIGS_DIR_NAME
        / f"{training_config}{CONFIG_FILE_EXTENSION}"
    )
    return training_config_path


def get_evaluation_config_path(proj_dir: Path, evaluation_config: str) -> Path:
    # Add extension as was removed when displaying to users
    evaluation_config_path: Path = (
        proj_dir
        / EVALUATION_CONFIGS_DIR_NAME
        / f"{evaluation_config}{CONFIG_FILE_EXTENSION}"
    )
    return evaluation_config_path


def copy_example_training_config_file(
    proj_dir: Path, train_config_file_name=EXAMPLE_TRAINING_CONFIG_FILE_NAME
) -> None:
    shutil.copyfile(
        EXAMPLE_TRAINING_CONFIG,
        proj_dir
        / f"{TRAINING_CONFIGS_DIR_NAME}/{train_config_file_name}.{TRAINING_CONFIG_EXTENSION}",
    )


def copy_example_evaluation_config_file(
    proj_dir: Path, evaluation_config_file_name=EXAMPLE_EVALUATION_CONFIG_FILE_NAME
) -> None:
    shutil.copyfile(
        EXAMPLE_EVALUATION_CONFIG,
        proj_dir
        / f"{EVALUATION_CONFIGS_DIR_NAME}/{evaluation_config_file_name}.{EVALUATION_CONFIG_EXTENSION}",
    )


def check_training_config_exists(proj_dir: Path, training_config_name: str) -> bool:
    return (
        proj_dir
        / TRAINING_CONFIGS_DIR_NAME
        / f"{training_config_name}.{TRAINING_CONFIG_EXTENSION}"
    ).is_file()


def check_evaluation_config_exists(proj_dir: Path, evaluation_config_name: str) -> bool:
    return (
        proj_dir
        / EVALUATION_CONFIGS_DIR_NAME
        / f"{evaluation_config_name}.{EVALUATION_CONFIG_EXTENSION}"
    ).is_file()


def get_config_dict(path: pathlib.Path):
    config: dict[str, dict[str, str]] = {}

    config_parser = ConfigParser()
    config_parser.optionxform = str
    assert_config_file_exists(path)
    config_parser.read(path)

    for section in config_parser.sections():
        config[section] = dict(config_parser.items(section))

    return config
