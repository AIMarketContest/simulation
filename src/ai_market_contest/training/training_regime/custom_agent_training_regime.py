import pathlib
from typing import Final, Union

import typer
from ray.rllib.agents.trainer import Trainer

from ai_market_contest.agent import Agent
from ai_market_contest.agents.trainer_agent_adapter import TrainerAgentAdapter
from ai_market_contest.cli.cli_config import TRAINED_PICKLE_FILENAME
from ai_market_contest.cli.configs.agent_config_reader import AgentConfigReader
from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.execute_training_routine import create_trained_agent_dir
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.training import get_agent_price_dict
from ai_market_contest.environment import Market
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)
from ai_market_contest.training.training_regime.training_regime import TrainingRegime

# Assumes agent to train is always first in the list
MAIN_AGENT_INDEX: Final = 0


class CustomAgentTrainingRegime(TrainingRegime):
    def __init__(
        self,
        training_config: TrainingConfigReader,
        project_dir: pathlib.Path,
        agent_version: ExistingAgentVersion,
        training_msg: str,
        agent_config_reader: AgentConfigReader,
    ):
        self.training_config_reader = training_config
        self.project_dir = project_dir
        self.agent_version = agent_version
        self.training_msg = training_msg
        self.agent_config_reader = agent_config_reader

    def execute(self) -> None:
        agent_name_maker: AgentNameMaker = SequentialAgentNameMaker(
            self.training_config_reader.get_num_agents()
        )
        env: Market = self.training_config_reader.get_environment(agent_name_maker)

        # Assumes agent to train is always first in the list
        agents: list[Agent]
        self_play_agents: list[Agent]
        agents, self_play_agents, _, _ = self._get_agents_in_simulation(
            env, agent_name_maker
        )

        epochs = self.training_config_reader.get_epochs()
        cumulative_profits: list[int] = []
        for epoch in range(epochs):
            profit: int = self._simulation(agents, env, self_play_agents)
            cumulative_profits.append(profit)

            self._display_information_on_current_epoch(epoch, cumulative_profits)

        self._save_new_custom_agent(agents[MAIN_AGENT_INDEX])

    def _get_agents_in_simulation(
        self, environment: Market, agent_name_maker: AgentNameMaker
    ) -> tuple[list[Agent], list[Agent], list[Agent], list[Agent]]:
        self_play_agents: list[
            Agent
        ] = self.training_config_reader.get_self_play_agents(self.agent_version)
        naive_agents: list[Agent] = self.training_config_reader.get_naive_agents()
        trained_agents: list[
            Union[Agent, Trainer]
        ] = self.training_config_reader.get_trained_agents(
            self.project_dir, environment
        )

        trained_agents: list[Agent] = list(
            map(
                lambda agent: TrainerAgentAdapter.convert_if_trainer(
                    agent, agent_name_maker.get_names()
                ),
                trained_agents,
            )
        )

        agents: list[Agent] = []
        agents.extend(self_play_agents)
        agents.extend(naive_agents)
        agents.extend(trained_agents)

        return agents, self_play_agents, naive_agents, trained_agents

    def _simulation(
        self, agents: list[Agent], environment: Market, self_play_agents: list[Agent]
    ) -> int:
        current_prices: dict[str, int] = self._get_initial_prices(agents, environment)

        cumulative_profit = 0
        for _ in range(environment.simulation_length):
            profit = self._simulation_step(
                agents, environment, current_prices, self_play_agents
            )
            cumulative_profit += profit

        return cumulative_profit

    def _get_initial_prices(
        self, agents: list[Agent], environment: Market
    ) -> dict[str, int]:
        current_prices: dict[str, int] = {}

        for agent, agent_name in zip(agents, environment.agents):
            current_prices[agent_name] = agent.get_initial_price()

        return current_prices

    def _simulation_step(
        self,
        agents: list[Agent],
        environment: Market,
        current_prices: dict[str, int],
        self_play_agents: list[Agent],
    ) -> int:
        current_prices = get_agent_price_dict(agents, environment, current_prices)
        _, rewards, _, _ = environment.step(current_prices)
        self._teach_self_play_agents(self_play_agents, rewards, environment)
        return rewards[environment.agents[MAIN_AGENT_INDEX]]

    def _teach_self_play_agents(
        self,
        self_play_agents: list[Agent],
        rewards: dict[str, int],
        environment: Market,
    ) -> None:
        # index can be this way as self play agents always assumed at start of the list
        for index, agent in enumerate(self_play_agents):
            agent.update(rewards[environment.agents[index]], index)

    def _display_information_on_current_epoch(
        self, epoch: int, cumulative_profits: list[int]
    ) -> None:
        if self.training_config_reader.print_training():
            status = "epoch {:2d} \nreward min: {:6.2f}\nreward mean: {:6.2f}\nreward max:  {:6.2f}\n"
            typer.echo(
                status.format(
                    epoch + 1,
                    min(cumulative_profits),
                    sum(cumulative_profits) / len(cumulative_profits),
                    max(cumulative_profits),
                )
            )

    def _save_new_custom_agent(self, new_agent: Agent) -> None:
        new_agent_dir = create_trained_agent_dir(
            self.agent_version, self.training_msg, self.training_config_reader.get_config_file_path()
        )
        with open(new_agent_dir / TRAINED_PICKLE_FILENAME, "wb") as pickle_file:
            new_agent.save(pickle_file)
