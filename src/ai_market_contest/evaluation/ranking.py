from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np
import pytest

from ai_market_contest.agent import Agent
from ai_market_contest.evaluation.graphing import (
    create_agent_profits_dict,
    create_agents,
)


def cumulative_profit_ranking(
    agent_profits: Dict[str, List[int]]
) -> list[Tuple[str, int]]:
    cum_profits = get_cumulative_profits(agent_profits)
    cum_profit_items_sorted = sorted(
        cum_profits.items(), key=lambda pair: pair[1], reverse=True
    )
    return cum_profit_items_sorted


def get_cumulative_profits(agent_profits: Dict[str, List[int]]) -> Dict[str, int]:
    profits: Dict[str, int] = {}
    for (
        agent,
        agent_profit,
    ) in (
        agent_profits.items()
    ):  # for loop cycles through the agents and corresponding keys
        cum_profits = np.cumsum(agent_profit)
        profits[agent] = cum_profits[-1]

    return profits


def print_rankings(
    agents: List[Agent], names: List[str], rankings: list[Tuple[str, int]]
):

    agent_name_mapping = get_agent_name_mapping(agents, names)
    for (agent_name, cum_profit) in rankings:
        print(f"{agent_name_mapping[agent_name]} - {cum_profit}")


def get_agent_name_mapping(agents: List[Agent], names: List[str]):
    agent_name_mapping: Dict[str, str] = {}
    name_counts: Dict[str, int] = defaultdict(int)

    for agent, agent_name in zip(agents, names):
        agent_class_name = type(agent).__name__
        name_counts[agent_class_name] += 1
        agent_name_mapping[
            agent_name
        ] = f"{agent_class_name} {name_counts[agent_class_name]}"

    return agent_name_mapping


@pytest.mark.parametrize("num_agents", [124])
def test_graph_profits(num_agents):
    agents = create_agents(num_agents)
    agent_profits = create_agent_profits_dict(agents)
    cumulative_profit_ranking(agent_profits)
