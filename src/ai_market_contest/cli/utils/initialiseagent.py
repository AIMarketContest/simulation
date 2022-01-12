import configparser
import datetime
import pathlib
from string import Template
from typing import Any, Optional

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENT_FILE,
    AGENTS_DIR_NAME,
    CONFIG_FILENAME,
    TRAINED_AGENTS_DIR_NAME,
)
from ai_market_contest.cli.utils.filesystemutils import assert_config_file_exists
from ai_market_contest.cli.utils.hashing import get_agent_hash
from ai_market_contest.cli.utils.processmetafile import write_custom_agent_meta_file


def set_agent_to_initialised(agent_dir: pathlib.Path):
    config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    assert_config_file_exists(config_file)
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    config["training"]["initialised"] = "True"
    with config_file.open("w") as c_file:
        config.write(c_file)


def make_initial_trained_agent(agent_dir: pathlib.Path, initial_hash: str):
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
    extra_config: dict[Any, Any] = {},
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


def create_agent_dir(
    proj_dir: pathlib.Path, agent_name: str, overwrite_check: bool
) -> Optional[pathlib.Path]:
    agents_dir = proj_dir / AGENTS_DIR_NAME
    agent_dir: pathlib.Path = agents_dir / agent_name

    if agent_dir.exists() and overwrite_check:
        return None

    agent_dir.mkdir(parents=True, exist_ok=True)

    return agent_dir


def create_custom_agent_class(
    agent_name: str, proj_dir: pathlib.Path, overwrite_check: bool = False
):
    agent_dir = create_agent_dir(proj_dir, agent_name, overwrite_check)

    if agent_dir is None:
        return

    agent_filename: str = f"{agent_name}.py"
    agent_file: pathlib.Path = agent_dir / agent_filename
    agent_file.touch()
    create_new_agent_file(agent_file, agent_name)
    initial_hash: str = get_agent_hash()
    create_agent_config(agent_dir, initial_hash, "custom")
    make_initial_trained_agent(agent_dir, initial_hash)


def create_rllib_agent_config(proj_dir: pathlib.Path, type: str, name: str):
    agent_dir = create_agent_dir(proj_dir, name, False)

    if agent_dir is None:
        return

    initial_hash: str = get_agent_hash()
    create_agent_config(
        agent_dir,
        initial_hash,
        "rllib",
        {
            "rllib": {
                "agent_type": type,
            }
        },
    )
    make_initial_trained_agent(agent_dir, initial_hash)


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
