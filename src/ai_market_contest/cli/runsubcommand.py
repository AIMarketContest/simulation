import pathlib
import sys
from typing import Any

from ai_market_contest.agents.fixed_agent import FixedAgent
from ai_market_contest.agents.random_agent import RandomAgent
from ai_market_contest.cli.utils.run_contest import run_contest
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction
from ai_market_contest.demandfunctions.fixed_lowest_takes_all_demand_function import (
    LowestTakesAllDemandFunction,
)
from ai_market_contest.environment import Market
from ai_market_contest.evaluation.graphing import (
    graph_cumulative_profits,
    plot_average_step,
)


def run_simulation(args: Any):
    environment = Market(2, LowestTakesAllDemandFunction(), 50)
    agent1 = FixedAgent(25)
    agent2 = RandomAgent()

    agent_mapping = {agent1: "player_0", agent2: "player_1"}

    agent_sales = run_contest(environment, agent_mapping)

    plot_average_step(agent_sales, agent_mapping)
    graph_cumulative_profits(agent_sales, agent_mapping)


def create_subparser(subparsers: Any):  # type: ignore
    parser_train = subparsers.add_parser("run", help="Run a simulation")
    parser_train.add_argument("path", type=pathlib.Path, default=".")
    parser_train.set_defaults(func=run_simulation)
