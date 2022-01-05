import gym  # type: ignore
import pathlib  # type: ignore
from typing import Any, Dict  # type: ignore
from ray.rllib.agents.registry import get_trainer_class  # type: ignore
from ray.rllib.agents.trainer import Trainer  # type: ignore
from ray.tune.registry import register_env  # type: ignore


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

    def train(self, epochs: int, print_training: bool) -> None:
        for epoch in range(epochs):
            results = self.trainer.train()
            if print_training:
                self.pretty_print(results, epoch)

    def get_trainer(self):
        return self.trainer

    def pretty_print(self, results: Dict[str, Any], epochs: int) -> None:
        status = "{:2d} reward {:6.2f}/{:6.2f}/{:6.2f} len {:4.2f} saved {}"
        print(
            status.format(
                epoch + 1,
                result["episode_reward_min"],
                result["episode_reward_mean"],
                result["episode_reward_max"],
                result["episode_len_mean"],
            )
        )
