import configparser
import datetime
import pathlib
from string import Template
from typing import Any, Dict

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENT_FILE,
    AGENTS_DIR_NAME,
    CONFIG_FILENAME,
    TRAINED_AGENTS_DIR_NAME,
)
from ai_market_contest.cli.utils.filesystemutils import (
    assert_config_file_exists,
    check_overwrite,
)
from ai_market_contest.cli.utils.hashing import (
    get_agent_hash,
)
from ai_market_contest.cli.utils.processmetafile import write_custom_agent_meta_file


def set_agent_to_initialised(agent_dir: pathlib.Path):
    config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    assert_config_file_exists(config_file)
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    config["training"]["initialised"] = "True"
    with config_file.open("w") as c_file:
        config.write(c_file)


def make_initial_trained_agent(
    agent_dir: pathlib.Path, agent_name: str, initial_hash: str
):
    trained_agents_dir = agent_dir / TRAINED_AGENTS_DIR_NAME
    initial_trained_agent_dir = trained_agents_dir / initial_hash
    initial_trained_agent_dir.mkdir(parents=True)
    msg = "Initial untrained agent"
    write_custom_agent_meta_file(
        initial_trained_agent_dir, initial_hash, datetime.datetime.now(), msg
    )


def create_agent_config(
    agent_dir: pathlib.Path,
    initial_hash: str,
    type: str,
    extra_config: Dict[Any, Any] = {},
):
    agent_config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    config["general"] = {
        "type": type,
    }

    config["training"] = {
        "initial-hash": initial_hash,
        "trained-agents": str([initial_hash]),
        "initialised": "False",
    }

    for key, value in extra_config.items():
        config[key] = value

    with agent_config_file.open("w") as acf:
        config.write(acf)
    return initial_hash


def create_custom_agent_class(
    agent_name: str, proj_dir: pathlib.Path, overwrite_check: bool = False
):
    agents_dir = proj_dir / AGENTS_DIR_NAME
    agent_filename: str = f"{agent_name}.py"
    agent_dir: pathlib.Path = agents_dir / agent_name

    if (
        agent_dir.exists()
        and overwrite_check
        and not check_overwrite(agent_filename, agent_dir)
    ):
        return

    agent_file: pathlib.Path = agent_dir / agent_filename
    agent_dir.mkdir(parents=True, exist_ok=True)
    agent_file.touch()
    create_new_agent_file(agent_file, agent_name)
    initial_hash: str = get_agent_hash()
    create_agent_config(agent_dir, initial_hash, "custom")
    make_initial_trained_agent(agent_dir, agent_name, initial_hash)


def create_rllib_agent(proj_dir: pathlib.Path, type: str, name: str):
    agents_dir = proj_dir / AGENTS_DIR_NAME
    agent_dir: pathlib.Path = agents_dir / name

    if agent_dir.exists():
        return

    agent_dir.mkdir(parents=True, exist_ok=True)
    initial_hash: str = get_agent_hash()
    create_agent_config(agent_dir, initial_hash, "rllib")


def make_agent_classname_camelcase(agent_name: str):
    AGENT_STR = "agent"
    if AGENT_STR.capitalize() in agent_name:
        return agent_name
    agent_name_cc = agent_name.lower()
    if AGENT_STR in agent_name_cc:
        agent_name_cc = agent_name_cc.replace(AGENT_STR, AGENT_STR.capitalize())
    return agent_name_cc[0].upper() + agent_name_cc[1:]


def create_new_agent_file(agent_file: pathlib.Path, agent_name: str):
    subs: dict[str, str] = {
        "agent_classname": make_agent_classname_camelcase(agent_name)
    }
    with AGENT_FILE.open("r") as a_file:
        src = Template(a_file.read())
    with agent_file.open("w") as new_agent_file:
        new_agent_file.write(src.substitute(subs))
