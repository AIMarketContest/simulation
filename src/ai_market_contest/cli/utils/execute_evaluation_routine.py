import pathlib

from ai_market_contest.cli.cli_config import AGENTS_DIR_NAME, ENVS_DIR_NAME
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

    naive_agents = evaluation_config_reader.get_naive_agents()
    trained_agents = evaluation_config_reader.get_trained_agents(proj_dir)

    main_agent = agent_locator.get_agent_class_or_pickle(agent_version)
    agents = [main_agent] + naive_agents + trained_agents

    agent_name_maker = SequentialAgentNameMaker(len(agents))
    env = evaluation_config_reader.get_environment(agent_name_maker)

    results: dict[str, dict[str, list[int]]] = {
        "prices": {agent_name: [] for agent_name in env.agents},
        "rewards": {agent_name: [] for agent_name in env.agents},
    }

    current_prices: dict[str, int] = {}
    for (agent, agent_name) in zip(agents, env.agents):
        current_prices[agent_name] = agent.get_initial_price()

    for _ in range(env.simulation_length):
        current_prices = get_agent_price_dict(agents, env, current_prices)
        _, rewards, _, _ = env.step(current_prices)

        for agent_name, price in current_prices.items():
            results["prices"][agent_name].append(price)

        for agent_name, reward in rewards.items():
            results["rewards"][agent_name].append(reward)

    cumulative_rewards = cumulative_profit_ranking(results["rewards"])
    print_rankings(agents, env.agents, cumulative_rewards)
    agent_name_mapping = get_agent_name_mapping(agents, env.agents)
    graph_cumulative_profits(results["rewards"], agent_name_mapping)
