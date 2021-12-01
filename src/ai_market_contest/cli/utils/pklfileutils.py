import pathlib
import pickle
import shutil
import subprocess
import sys

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENT_PKL_FILENAME,
    COMMAND_NAME,
    INITIAL_PICKLE_FILE_NAME,
    INITIAL_PICKLER_NAME,
    PICKLE_FILENAME,
    TRAINED_AGENTS_DIR_NAME,
)
from ai_market_contest.cli.utils.filesystemutils import check_file_exists
from ai_market_contest.cli.utils.hashing import get_agent_initial_hash


def initialise_agent_pkl_file(agent_dir: pathlib.Path, show_traceback: bool):
    initial_pickler_file = agent_dir / INITIAL_PICKLER_NAME
    if show_traceback:
        res = subprocess.run(
            ["python3", initial_pickler_file.resolve()],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            universal_newlines=True,
        )
    else:
        res = subprocess.run(
            ["python3", initial_pickler_file.resolve()],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    if res.returncode != 0:
        print(
            f"Fix error in initial_pickler.py then re-run {COMMAND_NAME} initialise-agent <path>"
        )
        sys.exit(res.returncode)
    pickle_file = agent_dir / INITIAL_PICKLE_FILE_NAME
    pickle_file.touch()
    initial_agent_dir = (
        agent_dir / TRAINED_AGENTS_DIR_NAME / get_agent_initial_hash(agent_dir)
    )
    shutil.move(pickle_file, initial_agent_dir / PICKLE_FILENAME)


def get_agent_pkl_file(path: pathlib.Path, trained_agent_hash: str):
    agent_pkl_file: pathlib.Path = path / AGENT_PKL_FILENAME
    error_msg = (
        f"Error: agent {trained_agent_hash} has no agent.pkl file in its directory"
    )
    check_file_exists(agent_pkl_file, error_msg)
    return agent_pkl_file


def write_pkl_file(new_agent_dir: pathlib.Path, agent: Agent):
    pkl_file = new_agent_dir / PICKLE_FILENAME
    with pkl_file.open("wb") as pkl:
        pickle.dump(agent, pkl)
