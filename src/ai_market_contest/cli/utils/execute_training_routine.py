import datetime
import pathlib
from configparser import ConfigParser
from typing import Any, Dict

import gym
from ray.rllib.agents.registry import get_trainer_class  # type: ignore
from ray.rllib.agents.trainer import Trainer  # type: ignore

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    ENVS_DIR_NAME,
    TRAINED_AGENTS_DIR_NAME,
)
from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.checkpoint_locator import (
    get_checkpoint_path,
)
from ai_market_contest.cli.utils.config_utils import get_training_config_path
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.get_agents import (  # type: ignore
    add_trained_agent_to_config_file,
)
from ai_market_contest.cli.utils.hashing import hash_string  # type: ignore
from ai_market_contest.cli.utils.processmetafile import write_meta_file
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.agent_trainer import AgentTrainer
from ai_market_contest.training.custom_agent_trainer import CustomAgentTrainer
from ai_market_contest.training.rllib_agent_trainer import RLlibAgentTrainer
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,  # type: ignore
)
from ai_market_contest.training.training_config_maker import TrainingConfigMaker


def set_up_and_execute_training_routine(
    training_config: str,
    proj_dir: pathlib.Path,
    agent_version: ExistingAgentVersion,
    parent_hash: str,
    training_msg: str,
):
    training_config_path: pathlib.Path = get_training_config_path(
        proj_dir, training_config
    )
    config_parser: ConfigParser = ConfigParser()
    config_parser.optionxform = str
    env_dir = proj_dir / ENVS_DIR_NAME
    demand_function_locator: DemandFunctionLocator = DemandFunctionLocator(env_dir)
    config_reader: TrainingConfigReader = TrainingConfigReader(
        training_config_path, demand_function_locator, config_parser
    )
    agent_locator: AgentLocator = AgentLocator(proj_dir / AGENTS_DIR_NAME)
    agent_name_maker: AgentNameMaker = SequentialAgentNameMaker(
        config_reader.get_num_agents()
    )
    trainer = get_trainer(agent_version, config_reader, agent_locator, agent_name_maker)
    trainer.train(config_reader.get_num_epochs(), True)
    if not agent_version.was_agent_initialised():
        trainer.save(agent_version.get_dir())
        config_reader.write_config_to_file(agent_version.get_dir())

    save_new_agent(
        trainer,
        agent_version,
        parent_hash,
        training_msg,
        config_reader,
    )


def get_rllib_trainer(
    agent_version: ExistingAgentVersion,
    config_reader: TrainingConfigReader,
    agent_locator: AgentLocator,
    agent_name_maker: AgentNameMaker,
) -> AgentTrainer:

    trainer_cls: Trainer = get_trainer_class(agent_version.get_agent_name())
    training_config_maker: TrainingConfigMaker = TrainingConfigMaker(
        config_reader, trainer_cls
    )

    config: Dict[str, Any] = training_config_maker.make_training_config()
    checkpoint_path = get_checkpoint_path(
        agent_version.get_dir(), agent_version.was_agent_initialised(), config_reader
    )
    trainer: AgentTrainer = RLlibAgentTrainer(
        config_reader.get_environment(agent_name_maker),
        config,
        checkpoint_path,
        agent_version.was_agent_initialised(),
        trainer_cls,
    )
    return trainer


def get_custom_trainer(
    agent_version: ExistingAgentVersion,
    config_reader: TrainingConfigReader,
    agent_locator: AgentLocator,
    agent_name_maker: AgentNameMaker,
) -> AgentTrainer:
    naive_agents_counts: Dict[str, int] = config_reader.get_naive_agent_counts()
    self_play_num: int = config_reader.get_self_play_num()
    env: gym.Env = config_reader.get_environment(agent_name_maker)
    return CustomAgentTrainer(
        env,
        agent_version,
        naive_agents_counts,
        self_play_num,
        agent_locator,
        agent_name_maker,
    )


def get_trainer(
    agent_version: ExistingAgentVersion,
    config_reader: TrainingConfigReader,
    agent_locator: AgentLocator,
    agent_name_maker: AgentNameMaker,
) -> AgentTrainer:
    if agent_version.is_rllib_agent():
        return get_rllib_trainer(
            agent_version,
            config_reader,
            agent_locator,
            agent_name_maker,
        )
    else:
        return get_custom_trainer(
            agent_version, config_reader, agent_locator, agent_name_maker
        )


def save_new_agent(
    trainer: AgentTrainer,
    agent_version: ExistingAgentVersion,
    parent_hash: str,
    training_msg: str,
    config_reader: TrainingConfigReader,
):
    cur_datetime: datetime.datetime = datetime.datetime.now()
    agent_dir: pathlib.Path = agent_version.get_agent_dir()
    new_agent_hash: str = hash_string(str(cur_datetime))
    new_agent_dir: pathlib.Path = agent_dir / TRAINED_AGENTS_DIR_NAME / new_agent_hash
    new_agent_dir.mkdir()
    add_trained_agent_to_config_file(agent_dir, new_agent_hash)
    write_meta_file(
        new_agent_dir, new_agent_hash, cur_datetime, training_msg, parent_hash
    )
    config_reader.write_config_to_file(new_agent_dir)
    trainer.save(new_agent_dir)
