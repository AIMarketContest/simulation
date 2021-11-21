import configparser
import datetime
from hashlib import sha1 as hashing_algorithm
import pathlib
import sys

from ai_market_contest.cli.utils.filesystemutils import check_config_file_exists
from ai_market_contest.cli.cli_config import (  # type: ignore
    HASH_LENGTH,
    CONFIG_FILENAME,
)


def hash_string(string: str):
    return hashing_algorithm(string.encode()).hexdigest()


def get_shortened_hashes(hashes: list[str]):
    return list(map(lambda hash: hash[:HASH_LENGTH], hashes))


def set_agent_initial_hash(agent_dir: pathlib.Path):
    agent_config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    initial_hash = hash_string(str(datetime.datetime.now()))
    config["training"] = {
        "initial-hash": initial_hash,
        "trained-agents": [initial_hash],
        "initialised": "False"
    }
    with agent_config_file.open("w") as acf:
        config.write(acf)
    return initial_hash


def get_agent_initial_hash(chosen_agent_dir: pathlib.Path):
    agent_config_file: pathlib.Path = chosen_agent_dir / CONFIG_FILENAME
    check_config_file_exists(agent_config_file)
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(agent_config_file)
    try:
        initial_hash = config["training"]["initial-hash"]
    except KeyError:
        print("Error: agent config missing an initial hash")
        sys.exit(1)
    return initial_hash
