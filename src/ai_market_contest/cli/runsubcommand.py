import pathlib
import sys
from typing import Any
from ai_market_contest.agents.fixed_agent import FixedAgent
from ai_market_contest.cli.utils.run_contest import run_contest
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction

from ai_market_contest.environment import Market


def run_simulation(args: Any):
    environment = Market(2, FixedDemandFunction(), 50)
    agent1 = FixedAgent(25)
    agent2 = FixedAgent(75)

    agent_mapping = {agent1 : "agent1", agent2 : "agent2"}

    run_contest(environment, agent_mapping)

def create_subparser(subparsers: Any):  # type: ignore
    parser_train = subparsers.add_parser(
        "run", help="Run a simulation"
    )
    parser_train.add_argument("path", type=pathlib.Path, default=".")
    parser_train.set_defaults(func=run_simulation)
