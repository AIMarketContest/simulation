import ast
import atexit
import configparser
import pathlib

import typer

from ai_market_contest.cli.cli_config import (  # type: ignore
    CONFIG_FILENAME,
    DEMAND_FUNCTION_DIR_NAME,
    ENVS_DIR_NAME,
)
from ai_market_contest.cli.utils.initialisedemandfunction import (
    create_demand_functon_class,
)


def edit_environment_config_file(env_name: str, proj_dir: pathlib.Path):
    config_file: pathlib.Path = proj_dir / ENVS_DIR_NAME / CONFIG_FILENAME
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_file)
    envs: list[str] = ast.literal_eval(config["environment"]["demandfunctions"])
    if env_name not in envs:
        envs.append(env_name)
    config["environment"]["demandfunctions"] = str(envs)
    with config_file.open("w") as c_file:
        config.write(c_file)


def remove_demand_function(demand_function_name: str, proj_dir: pathlib.Path):
    demand_function_dir = proj_dir / DEMAND_FUNCTION_DIR_NAME
    target_demand_function = demand_function_dir / f"{demand_function_name}.py"

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
    if not path.is_dir():
        typer.echo("Illegal argument: Argument must be an existing directory")
        raise typer.Exit(1)

    atexit.register(remove_demand_function, demand_function_name, path)
    create_demand_functon_class(demand_function_name, path, True)
    edit_environment_config_file(demand_function_name, path)
    atexit.unregister(remove_demand_function)
