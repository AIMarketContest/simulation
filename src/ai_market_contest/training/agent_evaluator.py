import gym  # type: ignore
import pathlib  # type: ignore
from typing import Any, Dict, List  # type: ignore
from ray.rllib.agents.registry import get_trainer_class  # type: ignore
from rllib.agents.trainer import Trainer  # type: ignore
from ray.tune.registry import register_env  # type: ignore
from ray.tune.logger import pretty_print  # type: ignore
from ai_market_contest.agent import Agent # type: ignore


class AgentEvaluator:
    def __init__(
        self,
        env: gym.Environment,
        naive_agents_counts: Dict[Agent, Any],
        checkpoint_paths: List[pathlib.Path],
        trainer_str: str = "DQN",
    ):
        register_env("marketplace", env)
        self.training_config["env"] = "marketplace"
        trainer_cls: Trainer = get_trainer_class(trainer_str)
        self.trainer: Trainer = trainer_cls(config=training_config)
        self.trainer.restore(checkpoint_path)

    def evaluate(self, epochs: int, print_training: bool = False) -> None:
        for _ in range(epochs):
            results = self.trainer.train()
            if print_training:
                pretty_print(results)

    def get_trainer(self):
        return self.trainer
