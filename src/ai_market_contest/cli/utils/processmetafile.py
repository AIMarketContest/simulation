import configparser
import datetime
import pathlib
import sys

from ai_market_contest.cli.cli_config import (  # type: ignore
    META_FILENAME,
    TRAINED_AGENTS_DIR_NAME,
)
from ai_market_contest.cli.utils.filesystemutils import (  # type: ignore
    check_directory_exists,
    check_file_exists,
)


def write_meta_file(
    path: pathlib.Path,
    trained_agent_hash: str,
    time: datetime.datetime,
    message: str,
    parent_hash: str = None,
):
    meta_file: pathlib.Path = path / META_FILENAME
    meta_file.touch()
    config: configparser.ConfigParser = configparser.ConfigParser()
    config["time"] = {
        "year": time.year,
        "month": time.month,
        "day": time.day,
        "hour": time.hour,
        "minute": time.minute,
        "second": time.second,
        "microsecond": time.microsecond,
    }
    config["trained-agent"] = {
        "hash": trained_agent_hash,
        "parent-hash": str(parent_hash),
        "message": message,
    }

    with meta_file.open("w") as m_file:
        config.write(m_file)


def read_meta_file(meta_file: pathlib.Path):
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(meta_file)
    try:
        year = int(config["time"]["year"])
        month = int(config["time"]["month"])
        day = int(config["time"]["day"])
        hour = int(config["time"]["hour"])
        minute = int(config["time"]["minute"])
        second = int(config["time"]["second"])
        microsecond = int(config["time"]["microsecond"])
    except KeyError:
        print("Error: Meta file missing time data")
        sys.exit(1)
    except ValueError:
        print("Error: time attribute must only contain numbers")
        sys.exit(1)
    try:
        time = datetime.datetime(year, month, day, hour, minute, second, microsecond)
    except ValueError:
        print("Error: date time in meta file represents an invalid datetime")
        sys.exit(1)
    try:
        trained_agent_hash = config["trained-agent"]["hash"]
    except KeyError:
        print("Error: Meta file missing the trained agent hash")
        sys.exit(1)
    try:
        message = config["trained-agent"]["message"]
    except KeyError:
        message = ""
    try:
        parent_hash = config["trained-agent"]["parent-hash"]
    except:
        parent_hash = None
    return (trained_agent_hash, time, message, parent_hash)


def get_trained_agent_metadata(agent_dir: pathlib.Path, trained_agent_name: str):
    trained_agents_dir: pathlib.Path = agent_dir / TRAINED_AGENTS_DIR_NAME
    trained_agent_dir: pathlib.Path = trained_agents_dir / trained_agent_name
    error_msg: str = f"Error: no folder exists for {trained_agent_name}"
    check_directory_exists(trained_agent_dir, error_msg)
    meta_file: pathlib.Path = trained_agent_dir / META_FILENAME
    error_msg: str = f"Error: no meta file exists for {trained_agent_name}"
    check_file_exists(meta_file, error_msg)
    return read_meta_file(meta_file)
