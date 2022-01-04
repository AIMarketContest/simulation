import ast
import atexit
import configparser
import pathlib
import shutil
from typing import Any


from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    CONFIG_FILENAME,
    DEMAND_FUNCTION_DIR_NAME,
    ENVS_DIR_NAME,
)
from ai_market_contest.cli.utils.initialiseagent import create_agent_class
from utils.initialisedemandfunction import create_demand_functon_class


def edit_environment_config_file(agent_name: str, proj_dir: pathlib.Path):
    config_file: pathlib.Path = proj_dir / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    agents: list[str] = ast.literal_eval(config["agent"]["agents"])
    if agent_name not in agents:
        agents.append(agent_name)
    config["agent"]["agents"] = str(agents)
    with config_file.open("w") as c_file:
        config.write(c_file)


def remove_demand_function(demand_function_name: str, proj_dir: pathlib.Path):
    demand_function_dir = proj_dir / DEMAND_FUNCTION_DIR_NAME
    target_demand_function = demand_function_dir / f"{agendemand_function_namet_nam}.py"

    if target_demand_function.exists():
        target_demand_function.unlink()

    config_file: pathlib.Path = proj_dir / ENVS_DIR_NAME / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    demand_functions: list[str] = ast.literal_eval(
        config["environment"]["demandfunctions"]
    )
    if demand_function_name in demand_functions:
        demand_functions.remove(demand_function_name)
    config["environment"]["demandfunctions"] = str(demand_functions)
    with config_file.open("w") as c_file:
        config.write(c_file)


def create_demand_function(path: pathlib.Path, demand_function_name: str):
    # TODO: Move these to main cli function
    # if not path.is_dir():
    #     typer.echo("Illegal argument: Argument must be an existing directory")
    #     raise typer.Exit(1)
    # proj_dir = path / PROJ_DIR_NAME
    # if not proj_dir.is_dir():
    #     typer.echo(
    #         """No project has been initialised in the directory.
    #         To initialise a project run aicontest init <path>"""
    #     )
    #     raise typer.Exit(1)
    atexit.register(remove_demand_function, demand_function_name, path)
    create_demand_functon_class(demand_function_name, path, True)
    edit_environment_config_file(demand_function_name, path)
    atexit.unregister(remove_demand_function)
