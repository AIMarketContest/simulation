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
    TRAINING_CONFIGS_DIR_NAME,
)
from ai_market_contest.cli.training_config.train_config import (  # type: ignore
    TrainConfig,
)
from ai_market_contest.cli.training_config.training import (  # type: ignore
    train as TRAINING_ALGORITHM,
)
from ai_market_contest.cli.utils.getagents import (  # type: ignore
    add_trained_agent_to_config_file,
)
from ai_market_contest.cli.utils.hashing import hash_string  # type: ignore
from ai_market_contest.cli.utils.pklfileutils import write_pkl_file  # type: ignore
from ai_market_contest.cli.utils.processmetafile import write_meta_file  # type: ignore
from ai_market_contest.environment import Environment  # type: ignore


def execute_training_routine(
    proj_dir: pathlib.Path,
    agent_dir: pathlib.Path,
    parent_hash: str,
    training_msg: str,
    agent_pkl_file: pathlib.Path,
    training_config: str,
):
    agent: Agent = fetch_instantiated_agent(agent_dir, agent_pkl_file)

    config: TrainConfig = get_training_config(proj_dir, training_config)
    env: Environment = config.create_environment(agent)

    TRAINING_ALGORITHM(env)

    new_agents: List[Agent] = [agent]
    new_agent: Agent
    for new_agent in new_agents:
        save_new_agent(new_agent, agent_dir, parent_hash, training_msg, config)


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


def get_training_config(proj_dir: pathlib.Path, training_config: str) -> TrainConfig:
    # Add .py as extension was removed when displaying to users
    training_config_file: pathlib.Path = (
        proj_dir / TRAINING_CONFIGS_DIR_NAME / (training_config + ".py")
    )

    spec: ModuleSpec = importlib.util.spec_from_file_location(
        training_config, training_config_file
    )
    if spec is None:
        raise Exception(
            f"Could not import training config file {training_config_file}."
        )
    config_module: ModuleType = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise Exception("Error in finding the required training config file")
    spec.loader.exec_module(config_module)  # type: ignore
    config: TrainConfig = config_module.get_config()  # type: ignore

    return config


def fetch_instantiated_agent(
    agent_dir: pathlib.Path, agent_pkl_file: pathlib.Path
) -> Agent:
    # Add agent definition to path so can unpickle instantiated version
    sys.path.insert(0, str(agent_dir.resolve()))
    with agent_pkl_file.open("rb") as pkl_file:
        agent: Agent = pickle.load(pkl_file)
    return agent
