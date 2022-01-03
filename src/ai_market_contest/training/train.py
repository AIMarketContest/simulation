import gym
from typing import Any, Dict
from ray.rllib.agents.registry import get_trainer_class
from rllib.agents.trainer import Trainer


class AgentTrainer:
    def __init__(
        self,
        env: gym.Environment,
        training_config: Dict[str, Any],
        trainer_str: str = "DQN",
    ):
        self.training_config = training_config
        register_env("marketplace", env)
        self.training_config["env"] = "marketplace"
        trainer_cls = get_trainer_class(trainer)
        self.trainer = trainer_cls(config=training_config)

    def train(epochs: int, print_training: bool = False) -> None:
        for _ in range(epochs):
            results = self.trainer.train()
            if print_training:
                pretty_print(results)
