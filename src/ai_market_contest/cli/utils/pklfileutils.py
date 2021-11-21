import pathlib
import shutil
from subprocess import call

from ai_market_contest.cli.cli_config import (  # type: ignore
    INITIAL_PICKLER_NAME,
    INITIAL_PICKLE_FILE_NAME,
    TRAINED_AGENTS_DIR_NAME,
    AGENT_PKL_FILENAME,
)
from ai_market_contest.cli.utils.hashing import get_agent_initial_hash

from ai_market_contest.cli.utils.filesystemutils import check_file_exists


def initialise_agent_pkl_file(agent_dir: pathlib.Path):
    initial_pickler_file = agent_dir / INITIAL_PICKLER_NAME
    call(["python3", initial_pickler_file.resolve()])
    pickle_file = agent_dir / INITIAL_PICKLE_FILE_NAME
    pickle_file.touch()
    initial_agent_dir = (
        agent_dir / TRAINED_AGENTS_DIR_NAME / get_agent_initial_hash(agent_dir)
    )
    shutil.move(pickle_file, initial_agent_dir / INITIAL_PICKLE_FILE_NAME)


def get_agent_pkl_file(path: pathlib.Path, trained_agent_hash: str):
    agent_pkl_file: pathlib.Path = path / AGENT_PKL_FILENAME
    error_msg = (
        f"Error: agent {trained_agent_hash} has no agent.pkl file in its directory"
    )
    check_file_exists(agent_pkl_file, error_msg)
    return agent_pkl_file
