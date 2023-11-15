import pathlib
from typing import Union

import typer
from ray.rllib.agents.trainer import Trainer

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import (
    AGENTS_DIR_NAME,
    DEFAULT_INITIAL_AGENT_PRICE,
    ENVS_DIR_NAME,
)
from ai_market_contest.cli.configs.agent_config_reader import AgentConfigReader
from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.config_utils import get_training_config_path
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.execute_training_routine import save_new_custom_agent
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.training import get_agent_price_dict
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)
from ai_market_contest.training.training_regime.training_regime import TrainingRegime


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
        # Assumes agent to train is always first in the list
        epochs = self.training_config_reader.get_epochs()
        agent_name_maker: AgentNameMaker = SequentialAgentNameMaker(
            self.training_config_reader.get_num_agents()
        )

        env = self.training_config_reader.get_environment(agent_name_maker)
        self_play_agents = self.training_config_reader.get_self_play_agents(
            self.agent_version
        )
        naive_agents = self.training_config_reader.get_naive_agents()
        trained_agents = self.training_config_reader.get_trained_agents(
            self.project_dir, env
        )

        agents: list[Union[Agent, Trainer]] = []
        agents.extend(self_play_agents + naive_agents)
        agents.extend(trained_agents)

        cumulative_profits: list[int] = []
        for epoch in range(epochs):
            current_prices: dict[str, int] = {}

            for agent, agent_name in zip(agents, env.agents):
                if isinstance(agent, Trainer):
                    current_prices[agent_name] = DEFAULT_INITIAL_AGENT_PRICE
                else:
                    current_prices[agent_name] = agent.get_initial_price()

            cumulative_profit = 0
            for _ in range(env.simulation_length):
                current_prices = get_agent_price_dict(agents, env, current_prices)
                _, rewards, _, _ = env.step(current_prices)
                for index, agent in enumerate(self_play_agents):
                    agent.update(rewards[env.agents[index]], index)

                cumulative_profit += rewards[env.agents[0]]

            cumulative_profits.append(cumulative_profit)

            if self.training_config_reader.print_training():
                status = "epoch {:2d} \nreward min: {:6.2f}\nreward mean: {:6.2f}\nreward max:  {:6.2f}\nmean length: {:4.2f}\n"
                typer.echo(
                    status.format(
                        epoch + 1,
                        min(cumulative_profits),
                        sum(cumulative_profits) / len(cumulative_profits),
                        max(cumulative_profits),
                        env.simulation_length,
                    )
                )

        save_new_custom_agent(
            self_play_agents[0],
            self.agent_version,
            self.training_msg,
            self.training_config_reader.get_config_file_path(),
        )
