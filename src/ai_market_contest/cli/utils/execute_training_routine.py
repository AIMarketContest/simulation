import datetime
import pathlib
import shutil
from typing import Union

import typer
from ray.rllib.agents.trainer import Trainer

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    DEFAULT_INITIAL_AGENT_PRICE,
    ENVS_DIR_NAME,
    TRAINED_AGENTS_DIR_NAME,
    TRAINED_CONFIG_FILENAME,
    TRAINED_PICKLE_FILENAME,
)
from ai_market_contest.cli.configs.agent_config_reader import (
    AgentConfigReader,  # type: ignore
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


def set_up_and_execute_rllib_training_routine(
    training_config_name: str,
    proj_dir: pathlib.Path,
    agent_version: ExistingAgentVersion,
    training_msg: str,
    agent_config_reader: AgentConfigReader,
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

    trainer = agent_locator.get_trainer(
        agent_version,
        env,
        agent_config_reader,
        training_config_reader.get_other_config(),
    )

    for epoch in range(epochs):
        results = trainer.train()

        if training_config_reader.print_training():
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

    save_new_rllib_trainer(trainer, agent_version, training_msg, training_config_path)


def create_trained_agent_dir(
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
    return new_agent_dir


def save_new_custom_agent(
    new_agent: Agent,
    old_agent_version: ExistingAgentVersion,
    training_msg: str,
    training_config_path: pathlib.Path,
):
    new_agent_dir = create_trained_agent_dir(
        old_agent_version, training_msg, training_config_path
    )
    with open(new_agent_dir / TRAINED_PICKLE_FILENAME, "wb") as pickle_file:
        new_agent.save(pickle_file)


def save_new_rllib_trainer(
    new_trainer: Trainer,
    old_agent_version: ExistingAgentVersion,
    training_msg: str,
    training_config_path: pathlib.Path,
):
    new_agent_dir = create_trained_agent_dir(
        old_agent_version, training_msg, training_config_path
    )
    new_trainer.save(new_agent_dir)
