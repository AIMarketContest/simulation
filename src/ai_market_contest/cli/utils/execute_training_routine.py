import datetime
import importlib.util
import pathlib
import pickle
import sys
from importlib.machinery import ModuleSpec
from io import BufferedReader
from types import ModuleType
from typing import List

from ai_market_contest.agent import Agent  # type: ignore
from ai_market_contest.cli.cli_config import (  # type: ignore
    TRAINED_AGENTS_DIR_NAME,
    TRAINING_CONFIG_FILE_EXTENSION,
    TRAINING_CONFIGS_DIR_NAME,
)
from ai_market_contest.cli.training_config.config_reader import TrainingConfigReader
from ai_market_contest.cli.training_config.training import (
    train as TRAINING_ALGORITHM,  # type: ignore
)
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.getagents import (  # type: ignore
    add_trained_agent_to_config_file,
)
from ai_market_contest.cli.utils.hashing import hash_string  # type: ignore
from ai_market_contest.cli.utils.pklfileutils import write_pkl_file  # type: ignore
from ai_market_contest.cli.utils.processmetafile import write_meta_file
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.policy_selector import PolicySelector
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,  # type: ignore
)


def set_up_and_execute_training_routine(
    training_config: str,
    proj_dir: pathlib.Path,
    agent_dir: pathlib.Path,
    agent_name: str,
    parent_hash: str,
    training_msg: str,
):
    training_config_path: pathlib.Path = get_training_config_path(
        proj_dir, training_config
    )
    demand_function_locator: DemandFunctionLocator = DemandFunctionLocator(proj_dir)
    config_reader: TrainingConfigReader = TrainingConfigReader(
        training_config_path, demand_function_locator
    )

    agent_name_maker: AgentNameMaker = SequentialAgentNameMaker(
        config_reader.get_num_agents()
    )

    policy_selector: PolicySelector = PolicySelector(
        agent_name,
        config_reader.get_self_play_num(),
        config_reader.get_naive_agent_counts(),
    )


def save_new_agent(new_agent, agent_dir, parent_hash, training_msg, config):
    cur_datetime: datetime.datetime = datetime.datetime.now()
    new_agent_hash: str = hash_string(str(cur_datetime))
    new_agent_dir: pathlib.Path = agent_dir / TRAINED_AGENTS_DIR_NAME / new_agent_hash
    new_agent_dir.mkdir()
    add_trained_agent_to_config_file(agent_dir, new_agent_hash)
    write_meta_file(
        new_agent_dir, new_agent_hash, cur_datetime, training_msg, parent_hash
    )
    write_pkl_file(new_agent_dir, new_agent)
    config.write_config_to_file(new_agent_dir)


def get_training_config_path(
    proj_dir: pathlib.Path, training_config: str
) -> pathlib.Path:
    # Add extension as was removed when displaying to users
    training_config_file_path: pathlib.Path = (
        proj_dir
        / TRAINING_CONFIGS_DIR_NAME
        / f"{training_config}{TRAINING_CONFIG_FILE_EXTENSION}"
    )
    return training_config_file_path


def fetch_instantiated_agent(
    agent_dir: pathlib.Path, agent_pkl_file: pathlib.Path
) -> Agent:
    # TODO replace with restore
    return None
