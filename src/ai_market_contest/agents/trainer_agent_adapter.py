from typing import Union

from ray.rllib.agents.trainer import Trainer

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import DEFAULT_INITIAL_AGENT_PRICE
from ai_market_contest.typing.types import Price


class TrainerAgentAdapter(Agent):
    def __init__(self, trainer: Trainer, agents_in_simulation: list[str]):
        self.trainer = trainer
        self.agents_in_simulation = agents_in_simulation

    @staticmethod
    def convert_if_trainer(
        trained_entity: Union[Agent, Trainer], agents_in_simulation: list[str]
    ) -> Agent:
        if isinstance(trained_entity, Trainer):
            return TrainerAgentAdapter(trained_entity, agents_in_simulation)
        return trained_entity

    def get_initial_price(self) -> Price:
        return DEFAULT_INITIAL_AGENT_PRICE

    def policy(
        self, last_round_all_agents_prices: list[Price], identity_index: int
    ) -> Price:
        observations = {
            agent_name: last_round_all_agents_prices
            for agent_name in self.agents_in_simulation
        }
        return self.trainer.compute_actions(observations)["player_0"]
