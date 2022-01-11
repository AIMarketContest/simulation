import pathlib  # type: ignore
from typing import Any, Dict  # type: ignore

import gym  # type: ignore
from ray.rllib.agents.trainer import Trainer  # type: ignore
from ray.tune.registry import register_env  # type: ignore

from ai_market_contest.training.agent_trainer import AgentTrainer  # type: ignore


class RLlibAgentTrainer(AgentTrainer):
    def __init__(
        self,
        env: gym.Env,
        training_config: Dict[str, Any],
        checkpoint_path: pathlib.Path,
        restored: bool,
        trainer_cls: Trainer,
    ):
        self.training_config: Dict[str, Any] = training_config
        register_env("marketplace", lambda x: env)
        self.training_config["env"] = "marketplace"
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

    def pretty_print(self, results: Dict[str, Any], epoch: int) -> None:
        status = "epoch {:2d} \nreward min: {:6.2f}\nreward mean: {:6.2f}\nreward max: {:6.2f}\nmean length: {:4.2f}\n"
        print(
            status.format(
                epoch + 1,
                results["episode_reward_min"],
                results["episode_reward_mean"],
                results["episode_reward_max"],
                results["episode_len_mean"],
            )
        )

    def save(self, checkpoint_dir: pathlib.Path):
        self.trainer.save(checkpoint_dir)
