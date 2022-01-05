import pathlib
import sys
from typing import Any

from ai_market_contest.agents.fixed_agent_random import FixedAgentRandom  # type: ignore
from ai_market_contest.agents.random_agent import RandomAgent  # type: ignore
from ai_market_contest.cli.utils.run_contest import run_contest  # type: ignore
from ai_market_contest.demandfunctions.fixed_demand_function import (
    FixedDemandFunction,  # type: ignore
)
from ai_market_contest.demandfunctions.fixed_lowest_takes_all_demand_function import (  # type: ignore
    LowestTakesAllDemandFunction,
)
from ai_market_contest.environment import Market  # type: ignore
from ai_market_contest.evaluation.graphing import (  # type: ignore
    graph_cumulative_profits,
    plot_average_step,
)
from ai_market_contest.training.agent_name_maker import AgentNameMaker
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)


def run_simulation(args: Any):
    num_agents: int = 2
    agent_name_maker: AgentNameMaker = SequentialAgentNameMaker(num_agents)
    environment = Market(
        num_agents, LowestTakesAllDemandFunction(), 50, agent_name_maker
    )
    agent1 = FixedAgentRandom(25)
    agent2 = RandomAgent()

    agent_mapping = {agent1: "player_0", agent2: "player_1"}

    agent_sales = run_contest(environment, agent_mapping)

    plot_average_step(agent_sales, agent_mapping)
    graph_cumulative_profits(agent_sales, agent_mapping)


def create_subparser(subparsers: Any):  # type: ignore
    parser_train = subparsers.add_parser("run", help="Run a simulation")
    parser_train.add_argument("path", type=pathlib.Path, default=".")
    parser_train.set_defaults(func=run_simulation)
