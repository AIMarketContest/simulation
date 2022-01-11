import configparser
import datetime
import pathlib
import typing
from string import Template

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENT_FILE,
    CONFIG_FILENAME,
    TRAINED_AGENTS_DIR_NAME,
)
from ai_market_contest.cli.utils.filesystemutils import check_config_file_exists
from ai_market_contest.cli.utils.processmetafile import write_meta_file


def set_agent_to_initialised(agent_dir: pathlib.Path):
    config_file: pathlib.Path = agent_dir / CONFIG_FILENAME
    check_config_file_exists(config_file)
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
    write_meta_file(
        initial_trained_agent_dir, initial_hash, datetime.datetime.now(), msg
    )


def create_new_agent_file(agent_file: pathlib.Path, agent_name: str):
    subs: typing.Dict[str, str] = {"agent_classname": agent_name}
    with AGENT_FILE.open("r") as a_file:
        src = Template(a_file.read())
    with agent_file.open("w") as new_agent_file:
        new_agent_file.write(src.substitute(subs))
