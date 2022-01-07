import pathlib
import shutil
from pathlib import Path
from typing import Dict, List

import questionary
import typer
from addagentsubcommand import create_agent
from adddemandfunctionsubcommand import create_demand_function
from cli_config import (
    AGENTS_DIR_NAME,
    COMMAND_NAME,
    PROJ_DIR_NAME,
    RLLIB_AGENTS,
    TRAINED_AGENTS_DIR_NAME,
)
from initsubcommand import initialise_file_structure
from utils.filesystemutils import check_path_exists, check_proj_dir_exists
from utils.initialisedemandfunction import create_demand_functon_class

from ai_market_contest.cli.utils.agent_check_utils import (
    check_agent_is_initialised,
    check_directory_exists_for_agent,
)
from ai_market_contest.cli.utils.config_utils import check_configs, get_training_configs
from ai_market_contest.cli.utils.execute_training_routine import (
    set_up_and_execute_training_routine,
)
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.getagents import (
    get_agent_names,
    get_trained_agents,
    get_trained_agents_info,
)

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
    create_demand_function(path, demand_function_name)


@app.command()
def train(
    path: Path = typer.Option(Path(f".", exists=True)), showtraceback: bool = False
):
    proj_dir: Path = path / PROJ_DIR_NAME
    check_path_exists(path)
    check_proj_dir_exists(proj_dir)

    agent_names: List[str] = get_agent_names(proj_dir)
    chosen_agent_name: str = questionary.select(
        "Choose an agent to train.", choices=agent_names
    ).ask()
    chosen_agent: ExistingAgent = ExistingAgent(chosen_agent_name, proj_dir)

    trained_agents: List[str] = get_trained_agents(chosen_agent.get_dir())
    trained_agents_info: List[str] = get_trained_agents_info(
        trained_agents, chosen_agent.get_dir()
    )
    chosen_trained_agent: str = questionary.select(
        "Select which version of the agent to train", choices=trained_agents_info
    ).ask()
    chosen_agent_version: ExistingAgentVersion = ExistingAgentVersion(
        chosen_agent, chosen_trained_agent
    )
    training_configs: List[str] = get_training_configs(proj_dir)
    check_configs(training_configs)
    training_config: str = questionary.select(
        "Choose a training config:", choices=training_configs
    ).ask()

    training_msg: str = typer.prompt("Enter training message")

    # TODO replace None with current agent hash (as it becomes the parent)
    set_up_and_execute_training_routine(
        training_config,
        proj_dir,
        chosen_agent_version,
        chosen_trained_agent,
        training_msg,
    )


@app.command()
def evaluate(path: Path = typer.Option(Path(f".", exists=True))):
    proj_dir: Path = path / PROJ_DIR_NAME
    check_path_exists(path)
    check_proj_dir_exists(proj_dir)

    agents: Dict[str, ExistingAgentVersion] = {}

    agent_names: List[str] = get_agent_names(proj_dir)
    agent_names.append("exit")
    # TODO check that list is not empty
    while True:
        chosen_agent_name: str = questionary.select(
            "Choose an agent to train.", choices=agent_names
        ).ask()
        if chosen_agent_name == "exit":
            if not agents:
                print("Cannot start simulation with no trained agents")
                continue
            break
        chosen_agent: ExistingAgent = ExistingAgent(chosen_agent_name, proj_dir)

        trained_agents: List[str] = get_trained_agents(chosen_agent.get_dir())
        trained_agents_info: List[str] = get_trained_agents_info(
            trained_agents, chosen_agent.get_dir()
        )
        chosen_trained_agent: str = questionary.select(
            "Select which version of the agent to train", choices=trained_agents_info
        ).ask()
        chosen_agent_version: ExistingAgentVersion = ExistingAgentVersion(
            chosen_agent, chosen_trained_agent
        )
        agent_given_name: str = questionary.text("Enter unique name for agent").ask()
        while agent_given_name in agents.keys():
            agent_given_name: str = questionary.text(
                "Name was already taken. Enter unique name for agent"
            ).ask()
        agents[agent_given_name] = chosen_agent_version
    print(agents)


if __name__ == "__main__":
    app()
