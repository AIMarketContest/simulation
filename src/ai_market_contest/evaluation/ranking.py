from collections import defaultdict
from typing import Union

import numpy as np
from ray.rllib.agents.trainer import Trainer

from ai_market_contest.agent import Agent


def cumulative_profit_ranking(
    agent_profits: dict[str, list[int]]
) -> list[tuple[str, int]]:
    cum_profits = get_cumulative_profits(agent_profits)
    cum_profit_items_sorted = sorted(
        cum_profits.items(), key=lambda pair: pair[1], reverse=True
    )
    return cum_profit_items_sorted


def get_cumulative_profits(agent_profits: dict[str, list[int]]) -> dict[str, int]:
    profits: dict[str, int] = {}
    for (
        agent,
        agent_profit,
    ) in (
        agent_profits.items()
    ):  # for loop cycles through the agents and corresponding keys
        cum_profits = np.cumsum(agent_profit)
        profits[agent] = cum_profits[-1]

    return profits


def print_rankings(rankings: list[tuple[str, int]], agent_name_mapping: dict[str, str]):
    for agent_name, cum_profit in rankings:
        print(f"{agent_name_mapping[agent_name]} - {cum_profit}")


def get_agent_name_mapping(agents: list[Union[Agent, Trainer]], names: list[str]):
    agent_name_mapping: dict[str, str] = {}
    name_counts: dict[str, int] = defaultdict(int)

    for agent, agent_name in zip(agents, names):
        agent_class_name = agent.__class__.__name__
        name_counts[agent_class_name] += 1
        agent_name_mapping[
            agent_name
        ] = f"{agent_class_name} {name_counts[agent_class_name]}"

    return agent_name_mapping
