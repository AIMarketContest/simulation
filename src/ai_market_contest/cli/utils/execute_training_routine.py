import copy
import datetime
import pathlib
from typing import Dict, List

import shutil

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import (  # type: ignore
    AGENTS_DIR_NAME,
    ENVS_DIR_NAME,
    TRAINED_AGENTS_DIR_NAME,
    TRAINED_CONFIG_FILENAME,
    TRAINED_PICKLE_FILENAME,
)
from ai_market_contest.cli.configs.training_config_reader import TrainingConfigReader
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.config_utils import (
    get_training_config_path,
)
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.get_agents import (  # type: ignore
    add_trained_agent_to_config_file,
)
from ai_market_contest.cli.utils.hashing import (  # type: ignore
    get_agent_hash,
)
from ai_market_contest.cli.utils.processmetafile import write_custom_agent_meta_file
from ai_market_contest.cli.utils.training import get_agent_price_dict
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,  # type: ignore
)


def set_up_and_execute_training_routine(
    training_config_name: str,
    proj_dir: pathlib.Path,
    agent_version: ExistingAgentVersion,
    parent_hash: str,
    training_msg: str,
):
    # Assumes agent to train is always first in the list
    agents: List[Agent] = []

    agent_locator: AgentLocator = AgentLocator(proj_dir / AGENTS_DIR_NAME)
    demand_function_locator = DemandFunctionLocator(proj_dir / ENVS_DIR_NAME)

    training_config_path: pathlib.Path = get_training_config_path(
        proj_dir, training_config_name
    )
    training_config_reader = TrainingConfigReader(
        training_config_path, demand_function_locator
    )

    epochs = training_config_reader.get_epochs()

    # Adding one here as we must always have the agent to train

    main_agent = agent_locator.get_agent_class_or_pickle(agent_version)

    for _ in range(training_config_reader.get_self_play_num()):
        agents.append(copy.deepcopy(main_agent))

    for (agent_name, num) in training_config_reader.get_naive_agent_counts().items():
        agent = agent_locator.get_agent(agent_name)
        for _ in range(int(num)):
            agents.append(copy.deepcopy(agent()))

    for (
        agent_name,
        (agent_hash, num),
    ) in training_config_reader.get_trained_agent_counts().items():
        trained_exisiting_agent = ExistingAgent(agent_name, proj_dir)
        trained_agent_version = ExistingAgentVersion(
            trained_exisiting_agent, agent_hash
        )
        agent = agent_locator.get_agent_class_or_pickle(trained_agent_version)
        for _ in range(num):
            agents.append(copy.deepcopy(agent))

    agent_name_maker = SequentialAgentNameMaker(len(agents))
    env = training_config_reader.get_environment(agent_name_maker)

    cumulative_profits: List[int] = []

    for epoch in range(epochs):
        current_prices: Dict[str, int] = {}

        for (agent, agent_name) in zip(agents, env.agents):
            current_prices[agent_name] = agent.get_initial_price()

        cumulative_profit = 0
        for _ in range(env.simulation_length):
            current_prices = get_agent_price_dict(agents, env, current_prices)
            _, rewards, _, _ = env.step(current_prices)
            for index, agent in enumerate(agents):
                agent.update(rewards[env.agents[index]], index)

            cumulative_profit += rewards[env.agents[0]]

        cumulative_profits.append(cumulative_profit)

        if training_config_reader.print_training():
            status = "epoch {:2d} \nreward min: {:6.2f}\nreward mean: {:6.2f}\nreward max:  {:6.2f}\nmean length: {:4.2f}\n"
            typer.echo(
                status.format(
                    epoch + 1,
                    min(cumulative_profits),
                    sum(cumulative_profits) / len(cumulative_profits),
                    max(cumulative_profits),
                    env.simulation_length,
                )
            )


    # def set_up_and_execute_training_routine(
    #     training_config: str,
    #     proj_dir: pathlib.Path,
    #     agent_version: ExistingAgentVersion,
    #     parent_hash: str,
    #     training_msg: str,
    # ):
    #     training_config_path: pathlib.Path = get_training_config_path(
    #         proj_dir, training_config
    #     )
    #     config_parser: ConfigParser = ConfigParser()
    #     config_parser.optionxform = str
    #     env_dir = proj_dir / ENVS_DIR_NAME
    # demand_function_locator: DemandFunctionLocator = DemandFunctionLocator(env_dir)
    # agent_name_maker: AgentNameMaker = SequentialAgentNameMaker(
    #     config_reader.get_num_agents()
    # )


# policy_selector: PolicySelector = PolicySelector(
#     agent_version.get_agent_name(),
#     config_reader.get_self_play_num(),
#     config_reader.get_naive_agent_counts(),
# )

# agent_locator: AgentLocator = AgentLocator(proj_dir / AGENTS_DIR_NAME)

#     policy_config_maker: PolicyConfigMaker = PolicyConfigMaker(
#         agent_locator, policy_selector
#     )

#     training_config_maker: TrainingConfigMaker = TrainingConfigMaker(
#         config_reader, policy_config_maker
#     )

#     config: dict[str, Any] = training_config_maker.make_training_config()
#     checkpoint_path = get_checkpoint_path(
#         agent_version.get_dir(), agent_version.was_agent_initialised(), config_reader
#     )
#     trainer: AgentTrainer = AgentTrainer(
#         config_reader.get_environment(agent_name_maker),
#         config,
#         checkpoint_path,
#         agent_version.was_agent_initialised(),
#         config_reader.get_optimisation_algorithm(),
#     )
#     trainer.train(config_reader.get_num_epochs(), config_reader.print_training())
#     if not agent_version.was_agent_initialised():
#         trainer.save(agent_version.get_dir())
#         config_reader.write_config_to_file(agent_version.get_dir())
#     save_new_agent(
#         trainer,
#         agent_version,
#         parent_hash,
#         training_msg,
#         config_reader,
#         policy_config_maker,
#     )


def save_new_custom_agent(
    new_agent: Agent,
    old_agent_version: ExistingAgentVersion,
    training_msg: str,
    training_config_path: pathlib.Path,
):
    cur_datetime: datetime.datetime = datetime.datetime.now()
    agent_dir: pathlib.Path = old_agent_version.get_agent_dir()
    new_agent_hash: str = get_agent_hash()
    new_agent_dir: pathlib.Path = agent_dir / TRAINED_AGENTS_DIR_NAME / new_agent_hash
    new_agent_dir.mkdir()
    add_trained_agent_to_config_file(agent_dir, new_agent_hash)
    write_custom_agent_meta_file(
        new_agent_dir,
        new_agent_hash,
        cur_datetime,
        training_msg,
        old_agent_version.version,
    )
    shutil.copy(training_config_path, new_agent_dir / TRAINED_CONFIG_FILENAME)
    # policy_config_maker.save_multiagent_config(new_agent_dir)
    with open(new_agent_dir / TRAINED_PICKLE_FILENAME, "wb") as pickle_file:
        new_agent.save(pickle_file)
