import shutil
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List

import questionary
import typer
from adddemandfunctionsubcommand import create_demand_function
from cli_config import (
    AGENTS_DIR_NAME,
    COMMAND_NAME,
    ENVS_DIR_NAME,
    PROJ_DIR_NAME,
    RLLIB_AGENTS,
)
from utils.agent_locator import AgentLocator
from utils.filesystemutils import check_proj_dir_exists

from ai_market_contest.cli.agent_creators.agent_creator import (
    AgentCreator,  # type: ignore
)
from ai_market_contest.cli.agent_creators.custom_agent_creator import (
    CustomAgentCreator,  # type: ignore
)
from ai_market_contest.cli.agent_creators.rllib_agent_creator import (
    RLlibAgentCreator,  # type: ignore
)
from ai_market_contest.cli.configs.evaluation_config_reader import (
    EvaluationConfigReader,
)
from ai_market_contest.cli.file_structure_init import initialise_file_structure
from ai_market_contest.cli.utils.agent_manipulation_utils import create_agent
from ai_market_contest.cli.utils.config_utils import (
    check_configs_exist,
    get_evaluation_config_path,
    get_evaluation_configs,
    get_training_configs,
)
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.execute_training_routine import (
    set_up_and_execute_training_routine,
)
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.get_agents import (
    get_agent_names,
    get_trained_agents,
    get_trained_agents_info,
)
from ai_market_contest.evaluation.agent_evaluator import AgentEvaluator
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
app = typer.Typer(context_settings=CONTEXT_SETTINGS)


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
        "What type of agent would you like to start with \
        (you can add more after initialising the project)?",
        choices=["custom", "rllib"],
    ).ask()
    if agent_type == "custom":
        agent_names: List[str] = []
        agent_names.append(typer.prompt("Enter custom agent name"))
        agent_creator: AgentCreator = CustomAgentCreator(path, agent_names)
    elif agent_type == "rllib":
        rllib_agent = questionary.select(
            "What rllib agent would you like to use?",
            choices=RLLIB_AGENTS,
        ).ask()
        agent_creator: AgentCreator = RLlibAgentCreator(path, [rllib_agent])
    
    initialise_file_structure(path, authors.split(","))
    agent_creator.create_agents()


@app.command()
def reset(path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))):
    # TODO: Check folder has a config before deleting
    check_proj_dir_exists(path)
    shutil.rmtree(path)


@app.command()
def add_agent(path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))):
    agent_type = questionary.select(
        "What type of agent would you like add?",
        choices=["custom", "rllib"],
    ).ask()

    if agent_type == "custom":
        agent_name = typer.prompt("Enter custom agent name")
        agent_creator: AgentCreator = CustomAgentCreator(path, [agent_name])
        typer.echo(f"Agent located in {path}/agents/{agent_name} directory")
    elif agent_type == "rllib":
        rllib_agent = questionary.select(
            "What rllib agent would you like to use?",
            choices=RLLIB_AGENTS,
        ).ask()
        agent_creator: AgentCreator = RLlibAgentCreator(path, [rllib_agent])

    agent_creator.create_agents()


@app.command()
def add_demand_function(
    path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))
):
    demand_function_name = typer.prompt("Enter custom demand function name")
    create_demand_function(path, demand_function_name)
    typer.echo(
        f"Demand function located in \
        {path}/environments/demandfunctions/{demand_function_name}.py"
    )


@app.command()
def train(
    path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True)),
    showtraceback: bool = False,
):
    check_proj_dir_exists(path)

    agent_names: List[str] = get_agent_names(path)
    chosen_agent_name: str = questionary.select(
        "Choose an agent to train.", choices=agent_names
    ).ask()
    chosen_agent: ExistingAgent = ExistingAgent(chosen_agent_name, path)

    trained_agents: List[str] = get_trained_agents(chosen_agent.get_dir())
    trained_agents_info: Dict[str, str] = get_trained_agents_info(
        trained_agents, chosen_agent.get_dir()
    )
    chosen_trained_agent: str = questionary.select(
        "Select which version of the agent to train",
        choices=list(trained_agents_info.keys()),
    ).ask()
    chosen_agent_version: ExistingAgentVersion = ExistingAgentVersion(
        chosen_agent, trained_agents_info[chosen_trained_agent]
    )
    training_configs: List[str] = get_training_configs(path)
    check_configs_exist(training_configs)
    training_config: str = questionary.select(
        "Choose a training config:", choices=training_configs
    ).ask()

    training_msg: str = typer.prompt("Enter training message")

    set_up_and_execute_training_routine(
        training_config,
        path,
        chosen_agent_version,
        trained_agents_info[chosen_trained_agent],
        training_msg,
    )


def validationthing(name):
    return False


@app.command()
def evaluate(path: Path = typer.Option(Path(f"./{PROJ_DIR_NAME}", exists=True))):
    check_proj_dir_exists(path)

    agents: Dict[str, ExistingAgentVersion] = {}

    agent_names: List[str] = get_agent_names(path)
    agent_names.append("exit")
    agent_count: int = 0
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
        chosen_agent: ExistingAgent = ExistingAgent(chosen_agent_name, path)

        trained_agents: List[str] = get_trained_agents(chosen_agent.get_dir())
        trained_agents_info: Dict[str, str] = get_trained_agents_info(
            trained_agents, chosen_agent.get_dir()
        )
        chosen_trained_agent: str = questionary.select(
            "Select which version of the agent to train",
            choices=list(trained_agents_info.keys()),
        ).ask()
        chosen_agent_version: ExistingAgentVersion = ExistingAgentVersion(
            chosen_agent, trained_agents_info[chosen_trained_agent]
        )
        agent_given_name: str = questionary.text(
            "Enter unique name for agent",
            validate=(lambda name: name and name not in agents.keys()),
        ).ask()
        agents[agent_given_name] = chosen_agent_version
        agent_count += 1

    evaluation_configs: List[str] = get_evaluation_configs(path)
    check_configs_exist(evaluation_configs)
    evaluation_config: str = questionary.select(
        "Choose an evaluation configuration:", choices=evaluation_configs
    ).ask()
    eval_config_parser: ConfigParser = ConfigParser()
    eval_config_parser.optionxform = str

    env_dir: Path = path / ENVS_DIR_NAME
    evaluation_config_reader: EvaluationConfigReader = EvaluationConfigReader(
        get_evaluation_config_path(path, evaluation_config),
        DemandFunctionLocator(env_dir),
        eval_config_parser,
        agent_count,
    )
    agent_name_maker: AgentNameMaker = SequentialAgentNameMaker(
        evaluation_config_reader.get_num_agents()
    )

    agent_locator: AgentLocator = AgentLocator(path / AGENTS_DIR_NAME)

    evaluator: AgentEvaluator = AgentEvaluator(
        evaluation_config_reader.get_environment(agent_name_maker),
        agent_locator,
        evaluation_config_reader.get_naive_agent_counts(),
        agents,
        evaluation_config_reader.get_optimisation_algorithm(),
        agent_name_maker,
    )

    print(evaluator.evaluate())


if __name__ == "__main__":
    app()
