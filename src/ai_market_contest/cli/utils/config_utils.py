import sys
from pathlib import Path
from typing import List

from ai_market_contest.cli.cli_config import TRAINING_CONFIGS_DIR_NAME


def check_configs(training_configs: List[str]) -> None:
    if not training_configs:
        print(
            "Operation aborted: no training configs have been defined in training_configs"
        )
        sys.exit(1)


def get_training_configs(proj_dir: Path):
    training_configs_dir = proj_dir / TRAINING_CONFIGS_DIR_NAME
    training_configs = []
    for training_config_file in training_configs_dir.rglob("*.ini"):
        training_configs.append(training_config_file.stem)
    return training_configs
