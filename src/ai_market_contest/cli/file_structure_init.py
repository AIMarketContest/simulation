import configparser
import pathlib

import typer

from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    COMMAND_NAME,
    CONFIG_FILENAME,
    DEMAND_FUNCTION_DIR_NAME,
    ENVS_DIR_NAME,
    EVALUATION_CONFIGS_DIR_NAME,
    PROJ_DIR_NAME,
    TRAINING_CONFIGS_DIR_NAME,
)
from ai_market_contest.cli.utils.config_utils import (
    copy_example_evaluation_config_file,
    copy_example_training_config_file,
)


def initialise_file_structure(path: pathlib.Path):
    proj_dir: pathlib.Path = path / PROJ_DIR_NAME
    make_proj_dir(proj_dir)
    make_environment_config_file(proj_dir)
    make_agents_config_file(proj_dir)
    copy_example_training_config_file(proj_dir)
    copy_example_evaluation_config_file(proj_dir)
    make_main_config_file(proj_dir)


def make_proj_dir(proj_dir: pathlib.Path):
    if proj_dir.is_dir():
        typer.echo(
            f"""{PROJ_DIR_NAME} project already initialised in the given directory
            To delete the current project run {COMMAND_NAME} reset <path>
            To add an agent to the project run {COMMAND_NAME} add-agent <path>"""
        )
        typer.Exit(code=1)
    agents_dir: pathlib.Path = proj_dir / AGENTS_DIR_NAME
    environments_dir: pathlib.Path = proj_dir / ENVS_DIR_NAME
    demand_function_dir: pathlib.Path = proj_dir / DEMAND_FUNCTION_DIR_NAME
    training_configs_dir: pathlib.Path = proj_dir / TRAINING_CONFIGS_DIR_NAME
    evaluation_configs_dir: pathlib.Path = proj_dir / EVALUATION_CONFIGS_DIR_NAME
    agents_dir.mkdir(parents=True)
    environments_dir.mkdir(parents=True)
    demand_function_dir.mkdir(parents=True)
    training_configs_dir.mkdir(parents=True)
    evaluation_configs_dir.mkdir(parents=True)


def make_environment_config_file(proj_dir: pathlib.Path):
    config: configparser.ConfigParser = configparser.ConfigParser()
    config["environment"] = {"demandfunctions": []}  # type: ignore
    c_file: pathlib.Path = proj_dir / ENVS_DIR_NAME / CONFIG_FILENAME
    c_file.touch()
    with c_file.open("w") as config_file:
        config.write(config_file)


def make_agents_config_file(proj_dir: pathlib.Path):
    config: configparser.ConfigParser = configparser.ConfigParser()
    config["general"] = {"customagents": [], "rllibagents": []}  # type: ignore
    c_file: pathlib.Path = proj_dir / AGENTS_DIR_NAME / CONFIG_FILENAME
    c_file.touch()
    with c_file.open("w") as config_file:
        config.write(config_file)


def make_main_config_file(proj_dir: pathlib.Path):
    config: configparser.ConfigParser = configparser.ConfigParser()
    config["general"] = {"authors": []}  # type: ignore
    c_file: pathlib.Path = proj_dir / CONFIG_FILENAME
    c_file.touch()
    with c_file.open("w") as config_file:
        config.write(config_file)
