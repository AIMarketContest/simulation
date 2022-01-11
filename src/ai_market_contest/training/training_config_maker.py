from typing import Any, Dict

from ray.rllib.agents.trainer import Trainer

from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader


class TrainingConfigMaker:
    def __init__(
        self,
        trainer_config_reader: TrainingConfigReader,
        trainer_cls: Trainer,
    ):
        self.training_config_reader: TrainingConfigReader = trainer_config_reader
        self.trainer_cls: Trainer = trainer_cls

    def make_training_config(self) -> Dict[str, Any]:
        config = self.trainer_cls.get_default_config()
        config.update(self.training_config_reader.get_other_config())
        return config
