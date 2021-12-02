import datetime
import importlib.util
import pathlib
import pickle
import sys

from ai_market_contest.cli.cli_config import (
    TRAINED_AGENTS_DIR_NAME,
    TRAINING_CONFIGS_DIR_NAME,
)
from ai_market_contest.cli.training_config.training import train as TRAINING_ALGORITHM
from ai_market_contest.cli.utils.getagents import add_trained_agent_to_config_file
from ai_market_contest.cli.utils.hashing import hash_string
from ai_market_contest.cli.utils.pklfileutils import write_pkl_file
from ai_market_contest.cli.utils.processmetafile import write_meta_file


def execute_training_routine(
    proj_dir: pathlib.Path,
    agent_dir: pathlib.Path,
    parent_hash: str,
    training_msg: str,
    agent_pkl_file: pathlib.Path,
    training_config: str,
):
    sys.path.insert(0, str(agent_dir.resolve()))
    with agent_pkl_file.open("rb") as pkl_file:
        agent = pickle.load(pkl_file)

    training_config_file = (
        proj_dir / TRAINING_CONFIGS_DIR_NAME / (training_config + ".py")
    )
    spec = importlib.util.spec_from_file_location(training_config, training_config_file)
    if spec is None:
        raise Exception(
            f"Could not import training config file {training_config_file}."
        )
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    config = config_module.get_config()
    env = config.create_environment(agent)
    TRAINING_ALGORITHM(env)
    new_agents = [agent]
    for new_agent in new_agents:
        cur_datetime: datetime.datetime = datetime.datetime.now()
        new_agent_hash: str = hash_string(str(cur_datetime))
        new_agent_dir: pathlib.Path = (
            agent_dir / TRAINED_AGENTS_DIR_NAME / new_agent_hash
        )
        new_agent_dir.mkdir()
        add_trained_agent_to_config_file(agent_dir, new_agent_hash)
        write_meta_file(
            new_agent_dir, new_agent_hash, cur_datetime, training_msg, parent_hash
        )
        write_pkl_file(new_agent_dir, new_agent)
        config.write_config_to_file(new_agent_dir)
