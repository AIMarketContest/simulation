import gym  # type: ignore
import pathlib  # type: ignore
from typing import Any, Dict  # type: ignore
from ray.rllib.agents.registry import get_trainer_class  # type: ignore
from ray.rllib.agents.trainer import Trainer  # type: ignore
from ray.tune.registry import register_env  # type: ignore
from ray.tune.logger import pretty_print  # type: ignore


class AgentTrainer:
    def __init__(
        self,
        env: gym.Env,
        training_config: Dict[str, Any],
        checkpoint_path: pathlib.Path,
        restored: bool,
        trainer_str: str = "DQN",
    ):
        self.training_config: Dict[str, Any] = training_config
        register_env("marketplace", lambda x: env)
        self.training_config["env"] = "marketplace"
        trainer_cls: Trainer = get_trainer_class(trainer_str)
        self.trainer: Trainer = trainer_cls(config=training_config)
        if restored:
            self.trainer.restore(checkpoint_path)

    def train(self, epochs: int, print_training: bool = False) -> None:
        for _ in range(epochs):
            results = self.trainer.train()
            if print_training:
                pretty_print(results)

    def get_trainer(self):
        return self.trainer
