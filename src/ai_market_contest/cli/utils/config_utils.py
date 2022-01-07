import sys
from pathlib import Path
from typing import List

from ai_market_contest.cli.cli_config import (
    CONFIG_FILE_EXTENSION,
    EVALUATION_CONFIGS_DIR_NAME,
    TRAINING_CONFIGS_DIR_NAME,
)


def check_configs_exist(training_configs: List[str]) -> None:
    if not training_configs:
        print(
            "Operation aborted: no training configs have been defined in training_configs"
        )
        sys.exit(1)


def get_configs(proj_dir: Path, config_directory_name: str) -> List[str]:
    configs_dir = proj_dir / config_directory_name
    configs = []
    for config_file in configs_dir.rglob(f"*{CONFIG_FILE_EXTENSION}"):
        configs.append(config_file.stem)
    return configs


def get_training_configs(proj_dir: Path) -> List[str]:
    return get_configs(proj_dir, TRAINING_CONFIGS_DIR_NAME)


def get_evaluation_configs(proj_dir: Path) -> List[str]:
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
