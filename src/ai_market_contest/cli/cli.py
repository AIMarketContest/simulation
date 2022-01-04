from pathlib import Path
import shutil
from typing import List
import typer
import questionary
from addagentsubcommand import create_agent
from cli_config import COMMAND_NAME, PROJ_DIR_NAME, RLLIB_AGENTS

from initsubcommand import initialise_file_structure
from utils.filesystemutils import check_proj_dir_exists


app = typer.Typer()


@app.command()
def init(path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}"))):
    # Path validation
    if path.is_dir():
        typer.echo(
            f"""{PROJ_DIR_NAME} project already initialised in the given directory
            To delete the current project run {COMMAND_NAME} reset <path>
            To add an agent to the project run {COMMAND_NAME} add-agent <path>"""
        )
        raise typer.Exit(code=1)

    authors = typer.prompt("Enter name(s) of the author(s)")

    agent_type = questionary.select(
        "What type of agent would you like to start with (you can add more after initialising the project)?",
        choices=["custom", "rllib"],
    ).ask()

    if agent_type == "custom":
        agent_names: List[str] = []
        agent_names.append(typer.prompt("Enter custom agent name"))
        initialise_file_structure(path, agent_names, authors.split(","))
    elif agent_type == "rllib":
        rllib_agent = questionary.select(
            "What rllib agent would you like to use?",
            choices=RLLIB_AGENTS,
        ).ask()


@app.command()
def reset(path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))):
    # TODO: Check folder has a config before deleting
    check_proj_dir_exists(path)
    shutil.rmtree(path)


@app.command()
def add_agent(path: Path = typer.Option(Path(f".", exists=True))):
    agent_type = questionary.select(
        "What type of agent would you like add?",
        choices=["custom", "rllib"],
    ).ask()

    if agent_type == "custom":
        agent_name = typer.prompt("Enter custom agent name")
        create_agent(path, agent_name)
    elif agent_type == "rllib":
        rllib_agent = questionary.select(
            "What rllib agent would you like to use?",
            choices=RLLIB_AGENTS,
        ).ask()


@app.command()
def add_demand_function(path: Path = typer.Option(Path(f".", exists=True))):
    demand_function_name = typer.prompt("Enter custom demand function name")


@app.command()
def train():
    typer.echo(f"Train agent")


@app.command()
def run():
    typer.echo(f"Run agent")


if __name__ == "__main__":
    app()
