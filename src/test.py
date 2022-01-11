import pathlib
import shutil
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List

import questionary
import tensorflow as tf
import typer

from ai_market_contest.cli.adddemandfunctionsubcommand import create_demand_function
from ai_market_contest.cli.agent_creators.agent_creator import (
    AgentCreator,  # type: ignore
)
from ai_market_contest.cli.agent_creators.custom_agent_creator import (
    CustomAgentCreator,  # type: ignore
)
from ai_market_contest.cli.agent_creators.rllib_agent_creator import (
    RLlibAgentCreator,  # type: ignore
)
from ai_market_contest.cli.cli_config import (
    AGENTS_DIR_NAME,
    COMMAND_NAME,
    ENVS_DIR_NAME,
    PROJ_DIR_NAME,
    RLLIB_AGENTS,
)
from ai_market_contest.cli.configs.evaluation_config_reader import (
    EvaluationConfigReader,
)
from ai_market_contest.cli.file_structure_init import initialise_file_structure
from ai_market_contest.cli.utils.agent_locator import AgentLocator
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
from ai_market_contest.cli.utils.filesystemutils import check_proj_dir_exists
from ai_market_contest.cli.utils.get_agents import (
    get_custom_agent_names,
    get_rllib_agents,
    get_trained_agents,
    get_trained_agents_info,
)
from ai_market_contest.evaluation.agent_evaluator import AgentEvaluator
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)

path = pathlib.Path.cwd() / "aicontest"
# authors = ["Ibby", "Matteo"]
# custom_agents = ["XAgent", "YAgent"]
# agent_creator = CustomAgentCreator(path, custom_agents)
# initialise_file_structure(path, authors)
# agent_creator.create_agents()

# # rllib_agent = ["PPO"]
# # agent_creator = RLlibAgentCreator(path, rllib_agent)

# print(get_custom_agent_names(path))
# print(get_rllib_agents(path))

chosen_agent_name = "XAgent"

chosen_agent = ExistingAgent(chosen_agent_name, path)
trained_agents = get_trained_agents(chosen_agent.get_dir())
trained_agents_info = get_trained_agents_info(trained_agents, chosen_agent.get_dir())
chosen_trained_agent = list(trained_agents_info.keys())[0]
chosen_agent_version = ExistingAgentVersion(
    chosen_agent, trained_agents_info[chosen_trained_agent], False
)
training_configs = get_training_configs(path)
print(training_configs)
training_msg = "test"
training_config = training_configs[0]
set_up_and_execute_training_routine(
    training_config,
    path,
    chosen_agent_version,
    trained_agents_info[chosen_trained_agent],
    training_msg,
)
