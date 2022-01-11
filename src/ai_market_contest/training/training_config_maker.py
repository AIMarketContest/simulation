from typing import Any

from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.training.policy_config_maker import PolicyConfigMaker


class TrainingConfigMaker:
    def __init__(
        self,
        trainer_config_reader: TrainingConfigReader,
        policy_config_maker: PolicyConfigMaker,
    ):
        self.training_config_reader: TrainingConfigReader = trainer_config_reader
        self.policy_config_maker: PolicyConfigMaker = policy_config_maker

    def make_training_config(self) -> dict[str, Any]:
        config: dict[str, Any] = self.policy_config_maker.get_policy_config()
        config.update(self.training_config_reader.get_other_config())
        config["prioritized_replay"] = False
        return config
