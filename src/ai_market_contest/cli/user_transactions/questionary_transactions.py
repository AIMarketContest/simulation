import pathlib
from typing import Optional

import ai_market_contest.cli.user_interactions.questionary_interactions as ask_user_to
from ai_market_contest.cli.cli_config import AGENTS_DIR_NAME, ENVS_DIR_NAME
from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.config_utils import (
    assert_configs_exist,
    get_training_config_path,
    get_training_configs,
)
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.filesystemutils import assert_proj_dir_exists
from ai_market_contest.cli.utils.get_agents import get_agent_names


def select_trained_agent(path: str) -> Optional[ExistingAgentVersion]:
    chosen_agent: Optional[ExistingAgent] = select_existing_agent(path)
    if not chosen_agent:
        return

    trained_agent: Optional[ExistingAgentVersion] = select_agent_version(chosen_agent)
    return trained_agent


def select_existing_agent(path: str) -> Optional[ExistingAgent]:
    assert_proj_dir_exists(path)
    agent_names: list[str] = get_agent_names(path)
    chosen_agent_name: str = ask_user_to.choose_an_agent_from(agent_names, "train")
    if not chosen_agent_name:
        return
    chosen_agent: ExistingAgent = ExistingAgent(chosen_agent_name, path)
    return chosen_agent


def select_agent_version(agent: ExistingAgent) -> ExistingAgentVersion:
    trained_agents_info: Optional[
        dict[str, str]
    ] = agent.get_all_trained_agents_information()
    if not trained_agents_info:
        return

    chosen_trained_agent: Optional[str] = ask_user_to.choose_an_agent_version_from(
        list(trained_agents_info.keys()), "train"
    )
    if not chosen_trained_agent:
        return

    chosen_agent_version: ExistingAgentVersion = ExistingAgentVersion(
        agent, trained_agents_info[chosen_trained_agent]
    )
    return chosen_agent_version


def select_training_configuration_name(path: str) -> Optional[str]:
    training_configs: list[str] = get_training_configs(path)
    assert_configs_exist(training_configs)
    training_config: Optional[str] = ask_user_to.choose_a_training_configuration(
        training_configs
    )
    return training_config


def select_training_configuration(path: str) -> Optional[TrainingConfigReader]:
    training_config_name: Optional[str] = select_training_configuration_name(path)
    if not training_config_name:
        return

    training_config_path: pathlib.Path = get_training_config_path(
        path, training_config_name
    )

    agent_locator: AgentLocator = AgentLocator(path / AGENTS_DIR_NAME)
    demand_function_locator = DemandFunctionLocator(path / ENVS_DIR_NAME)

    training_config = TrainingConfigReader(
        training_config_path, demand_function_locator, agent_locator
    )

    return training_config
