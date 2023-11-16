import configparser
import datetime
import pathlib
import sys
from hashlib import sha1 as hashing_algorithm

from ai_market_contest.cli.cli_config import (  # type: ignore
    CONFIG_FILENAME,
    HASH_LENGTH,
)
from ai_market_contest.cli.utils.error_codes import ErrorCodes
from ai_market_contest.cli.utils.filesystemutils import assert_config_file_exists


def hash_string(string: str):
    return hashing_algorithm(string.encode()).hexdigest()


def get_shortened_hashes(hashes: list[str]):
    return list(map(lambda hash: hash[:HASH_LENGTH], hashes))


def get_agent_hash():
    return hash_string(str(datetime.datetime.now()))


def get_agent_initial_hash(chosen_agent_dir: pathlib.Path):
    agent_config_file: pathlib.Path = chosen_agent_dir / CONFIG_FILENAME
    assert_config_file_exists(agent_config_file)
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(agent_config_file)
    try:
        initial_hash = config["training"]["initial-hash"]
    except KeyError:
        print("Error: agent config missing an initial hash")
        sys.exit(ErrorCodes.MISSING_INITIAL_HASH)
    return initial_hash
