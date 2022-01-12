import datetime
import pathlib
import shutil
from typing import Union

import typer
from ray.rllib.agents.trainer import Trainer

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    ENVS_DIR_NAME,
    TRAINED_AGENTS_DIR_NAME,
    TRAINED_CONFIG_FILENAME,
    TRAINED_PICKLE_FILENAME,
)
from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.config_utils import get_training_config_path
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.get_agents import (  # type: ignore
    add_trained_agent_to_config_file,
)
from ai_market_contest.cli.utils.hashing import get_agent_hash  # type: ignore
from ai_market_contest.cli.utils.processmetafile import write_custom_agent_meta_file
from ai_market_contest.cli.utils.training import get_agent_price_dict
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,  # type: ignore
)


def set_up_and_execute_training_routine(
    training_config_name: str,
    proj_dir: pathlib.Path,
    agent_version: ExistingAgentVersion,
    training_msg: str,
):
    # Assumes agent to train is always first in the list
    agent_locator: AgentLocator = AgentLocator(proj_dir / AGENTS_DIR_NAME)
    demand_function_locator = DemandFunctionLocator(proj_dir / ENVS_DIR_NAME)

    training_config_path: pathlib.Path = get_training_config_path(
        proj_dir, training_config_name
    )
    training_config_reader = TrainingConfigReader(
        training_config_path, demand_function_locator, agent_locator
    )

    epochs = training_config_reader.get_epochs()
    agent_name_maker = SequentialAgentNameMaker(training_config_reader.get_num_agents())
    env = training_config_reader.get_environment(agent_name_maker)
    self_play_agents = training_config_reader.get_self_play_agents(agent_version)
    naive_agents = training_config_reader.get_naive_agents()
    trained_agents = training_config_reader.get_trained_agents(proj_dir, env)

    agents: list[Union[Agent, Trainer]] = (
        self_play_agents + naive_agents + trained_agents
    )

    cumulative_profits: list[int] = []
    DEFAULT_INITIAL_PRICE = 50
    for epoch in range(epochs):
        current_prices: dict[str, int] = {}

        for (agent, agent_name) in zip(agents, env.agents):
            if isinstance(agent, Trainer):
                current_prices[agent_name] = DEFAULT_INITIAL_PRICE
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

        if training_config_reader.print_training():
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

    save_new_custom_agent(agents[0], agent_version, training_msg, training_config_path)


def save_new_custom_agent(
    new_agent: Agent,
    old_agent_version: ExistingAgentVersion,
    training_msg: str,
    training_config_path: pathlib.Path,
):
    cur_datetime: datetime.datetime = datetime.datetime.now()
    agent_dir: pathlib.Path = old_agent_version.get_agent_dir()
    new_agent_hash: str = get_agent_hash()
    new_agent_dir: pathlib.Path = agent_dir / TRAINED_AGENTS_DIR_NAME / new_agent_hash
    new_agent_dir.mkdir()
    add_trained_agent_to_config_file(agent_dir, new_agent_hash)
    write_custom_agent_meta_file(
        new_agent_dir,
        new_agent_hash,
        cur_datetime,
        training_msg,
        old_agent_version.version,
    )
    shutil.copy(training_config_path, new_agent_dir / TRAINED_CONFIG_FILENAME)
    with open(new_agent_dir / TRAINED_PICKLE_FILENAME, "wb") as pickle_file:
        new_agent.save(pickle_file)
