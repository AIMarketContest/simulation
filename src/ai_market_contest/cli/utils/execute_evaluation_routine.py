import pathlib
from typing import Union

from ray.rllib.agents.trainer import Trainer

from ai_market_contest.agent import Agent
from ai_market_contest.cli.cli_config import (
    AGENTS_DIR_NAME,
    DEFAULT_INITIAL_AGENT_PRICE,
    ENVS_DIR_NAME,
)
from ai_market_contest.cli.configs.agent_config_reader import AgentConfigReader
from ai_market_contest.cli.configs.evaluation_config_reader import (
    EvaluationConfigReader,
)
from ai_market_contest.cli.utils.agent_locator import AgentLocator
from ai_market_contest.cli.utils.config_utils import get_evaluation_config_path
from ai_market_contest.cli.utils.demand_function_locator import DemandFunctionLocator
from ai_market_contest.cli.utils.existing_agent.existing_agent_version import (
    ExistingAgentVersion,
)
from ai_market_contest.cli.utils.training import get_agent_price_dict
from ai_market_contest.evaluation.graphing import graph_cumulative_profits
from ai_market_contest.evaluation.ranking import (
    cumulative_profit_ranking,
    get_agent_name_mapping,
    print_rankings,
)
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)


def execute_evaluation_routine(
    evaluation_config_name: str,
    proj_dir: pathlib.Path,
    agent_version: ExistingAgentVersion,
):
    agent_locator: AgentLocator = AgentLocator(proj_dir / AGENTS_DIR_NAME)
    demand_function_locator = DemandFunctionLocator(proj_dir / ENVS_DIR_NAME)

    evaluation_config_path: pathlib.Path = get_evaluation_config_path(
        proj_dir, evaluation_config_name
    )

    evaluation_config_reader = EvaluationConfigReader(
        evaluation_config_path, demand_function_locator, agent_locator
    )

    agent_name_maker = SequentialAgentNameMaker(
        evaluation_config_reader.get_num_agents()
    )

    agent_config_reader = AgentConfigReader(agent_version)

    env = evaluation_config_reader.get_environment(agent_name_maker)
    naive_agents = evaluation_config_reader.get_naive_agents()
    trained_agents = evaluation_config_reader.get_trained_agents(proj_dir, env)

    if agent_config_reader.get_agent_type() == "rllib":
        main_agent = agent_locator.get_trainer(
            agent_version,
            env,
            agent_config_reader,
            evaluation_config_reader.get_other_config(),
        )
        if main_agent is None:
            return
    else:
        main_agent = agent_locator.get_agent_class_or_pickle(agent_version)

    agents: list[Union[Agent, Trainer]] = [main_agent]
    agents.extend(naive_agents)
    agents.extend(trained_agents)

    env = evaluation_config_reader.get_environment(agent_name_maker)

    results: dict[str, dict[str, list[int]]] = {
        "prices": {agent_name: [] for agent_name in env.agents},
        "rewards": {agent_name: [] for agent_name in env.agents},
    }

    current_prices: dict[str, int] = {}
    for agent, agent_name in zip(agents, env.agents):
        if isinstance(agent, Trainer):
            current_prices[agent_name] = DEFAULT_INITIAL_AGENT_PRICE
        else:
            current_prices[agent_name] = agent.get_initial_price()

    for _ in range(env.simulation_length):
        current_prices = get_agent_price_dict(agents, env, current_prices)
        _, rewards, _, _ = env.step(current_prices)

        for agent_name, price in current_prices.items():
            results["prices"][agent_name].append(price)

        for agent_name, reward in rewards.items():
            results["rewards"][agent_name].append(reward)

    cumulative_rewards = cumulative_profit_ranking(results["rewards"])
    agent_name_mapping = get_agent_name_mapping(agents, env.agents)

    print_rankings(cumulative_rewards, agent_name_mapping)
    graph_cumulative_profits(results["rewards"], agent_name_mapping)
