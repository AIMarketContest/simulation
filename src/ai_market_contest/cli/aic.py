import pathlib
from ast import literal_eval
from pathlib import Path

import questionary
import typer

from ai_market_contest.cli.adddemandfunctionsubcommand import create_demand_function
from ai_market_contest.cli.cli_config import (
    COMMAND_NAME,
    EVALUATION_CONFIG_EXTENSION,
    EVALUATION_CONFIGS_DIR_NAME,
    PROJ_DIR_NAME,
    RLLIB_AGENTS,
    TRAINING_CONFIG_EXTENSION,
    TRAINING_CONFIGS_DIR_NAME,
)
from ai_market_contest.cli.resetsubcommand import remove_proj_dir
from ai_market_contest.cli.utils.agent_manipulation_utils import (
    create_custom_agent,
    create_rllib_agent,
)
from ai_market_contest.cli.utils.config_utils import (
    assert_configs_exist,
    check_evaluation_config_exists,
    check_training_config_exists,
    copy_example_evaluation_config_file,
    copy_example_training_config_file,
    get_evaluation_configs,
    get_training_configs,
)
from ai_market_contest.cli.utils.execute_evaluation_routine import (
    execute_evaluation_routine,
)
from ai_market_contest.cli.utils.execute_training_routine import (
    set_up_and_execute_training_routine,
)
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.filesystemutils import (
    assert_proj_dir_exists,
    check_overwrite,
)
from ai_market_contest.cli.utils.get_agents import get_agent_names
from ai_market_contest.cli.utils.project_initialisation_utils import (
    initialise_file_structure,
)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def init(path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}"))):
    """
    Initialises a folder structure for a project
    """
    # Path validation
    if path.is_dir():
        typer.echo(
            f"""{PROJ_DIR_NAME} project already initialised in the given directory
            To delete the current project run {COMMAND_NAME} reset <path>
            To add an agent to the project run {COMMAND_NAME} add-agent <path>"""
        )
        raise typer.Exit(code=1)

    authors = typer.prompt("Enter name(s) of the author(s)")
    initialise_file_structure(path, authors.split(","))

    agent_type = questionary.select(
        "What type of agent would you like to start with (you can add more after initialising the project)?",
        choices=["custom", "rllib"],
    ).ask()

    if agent_type == "custom":
        custom_agent_name = typer.prompt("Enter custom agent name")
        create_custom_agent(path, custom_agent_name)

    elif agent_type == "rllib":
        rllib_agent = questionary.select(
            "What rllib agent would like to start with (you can add more after initialising the project)?",
            choices=RLLIB_AGENTS,
        ).ask()
        rllib_agent_name = typer.prompt("Enter a name to identify this agent")
        create_rllib_agent(path, rllib_agent, rllib_agent_name)


@app.command()
def reset(path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))):
    """
    Reset initialised project folder structure
    """
    remove_proj_dir(path)


@app.command()
def add_agent(path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))):
    """
    Adds an agent to an initialised project
    """
    agent_type = questionary.select(
        "What type of agent would you like add?",
        choices=["custom", "rllib"],
    ).ask()

    if agent_type == "custom":
        agent_name = typer.prompt("Enter custom agent name")
        create_custom_agent(path, agent_name)
        typer.echo(f"Agent located in {path}/agents/{agent_name} directory")
    elif agent_type == "rllib":
        rllib_agent = questionary.select(
            "What rllib agent would like use?",
            choices=RLLIB_AGENTS,
        ).ask()
        rllib_agent_name = typer.prompt("Enter a name to identify this agent")
        create_rllib_agent(path, rllib_agent, rllib_agent_name)


@app.command()
def add_demand_function(
    path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))
):
    """
    Adds an demand function to an initialised project
    """
    demand_function_name = typer.prompt("Enter custom demand function name")
    create_demand_function(path, demand_function_name)
    typer.echo(
        f"Demand function located in \
        {path}/environments/demandfunctions/{demand_function_name}.py"
    )


@app.command()
def add_train_config(
    path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))
):
    """
    Adds an training config to an initialised project
    """
    assert_proj_dir_exists(path)
    config_name = questionary.text(
        "Enter name for training configuration:", validate=(lambda name: len(name) > 0)
    ).ask()
    if check_training_config_exists(path, config_name) and not check_overwrite(
        f"{config_name}.{TRAINING_CONFIG_EXTENSION}", path / TRAINING_CONFIGS_DIR_NAME
    ):
        return
    copy_example_training_config_file(path, config_name)
    typer.echo(
        f"Training configuration file located in \
        {path}/{TRAINING_CONFIGS_DIR_NAME}/{config_name}.{TRAINING_CONFIG_EXTENSION}"
    )


@app.command()
def add_evaluate_config(
    path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))
):
    """
    Adds an evaluation config to an initialised project
    """
    assert_proj_dir_exists(path)
    config_name = questionary.text(
        "Enter name for evaluation configuration:",
        validate=(lambda name: len(name) > 0),
    ).ask()
    if check_evaluation_config_exists(path, config_name) and not check_overwrite(
        f"{config_name}.{EVALUATION_CONFIG_EXTENSION}",
        path / EVALUATION_CONFIGS_DIR_NAME,
    ):
        return
    copy_example_evaluation_config_file(path, config_name)
    typer.echo(
        f"Evaluation configuration file located in \
        {path}/{EVALUATION_CONFIGS_DIR_NAME}/{config_name}.{EVALUATION_CONFIG_EXTENSION}"
    )


def get_chosen_agent_version(path: pathlib.Path, action: str):
    agent_names: list[str] = get_agent_names(path)
    chosen_agent_name: str = questionary.select(
        f"Choose an agent to {action}.", choices=agent_names
    ).ask()
    chosen_agent: ExistingAgent = ExistingAgent(chosen_agent_name, path)
    agent_config = chosen_agent.get_config()

    try:
        trained_agents: list[str] = literal_eval(
            agent_config["training"]["trained-agents"]
        )

        trained_agents_info: dict[str, str] = chosen_agent.get_trained_agents_info(
            trained_agents
        )
        chosen_trained_agent: str = questionary.select(
            f"Select which version of the agent would you like to {action}",
            choices=list(trained_agents_info.keys()),
        ).ask()

        chosen_agent_version: ExistingAgentVersion = ExistingAgentVersion(
            chosen_agent, trained_agents_info[chosen_trained_agent]
        )

        return chosen_agent_version
    except KeyError:
        typer.echo("Chosen agent's config is malformed or missing")
        return None


@app.command()
def train(
    path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True)),
    showtraceback: bool = False,
):
    """
    Train an agent within a specified environment
    """
    assert_proj_dir_exists(path)

    chosen_agent_version = get_chosen_agent_version(path, "train")

    if chosen_agent_version is None:
        return

    training_configs: list[str] = get_training_configs(path)
    assert_configs_exist(training_configs)
    training_config: str = questionary.select(
        "Choose a training config:", choices=training_configs
    ).ask()
    training_msg: str = typer.prompt("Enter training message")

    set_up_and_execute_training_routine(
        training_config,
        path,
        chosen_agent_version,
        training_msg,
    )


@app.command()
def evaluate(path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))):
    """
    Evaluate an agent in a specified environment
    """
    assert_proj_dir_exists(path)

    chosen_agent_version = get_chosen_agent_version(path, "evaluate")

    if chosen_agent_version is None:
        return

    evaluation_configs: list[str] = get_evaluation_configs(path)
    assert_configs_exist(evaluation_configs)
    evaluation_config: str = questionary.select(
        "Choose an evaluation configuration:", choices=evaluation_configs
    ).ask()

    execute_evaluation_routine(evaluation_config, path, chosen_agent_version)


def run():
    app()


if __name__ == "__main__":
    app()
