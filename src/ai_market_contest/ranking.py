
from typing import List

import numpy as np
import pytest

from ai_market_contest.agent import Agent
from ai_market_contest.graphing import create_agents, create_agent_names_dict, create_agent_profits_dict


def cumulative_profit_ranking(agent_profits: dict[Agent:List[float]], agent_names: dict[Agent:str]) -> List[(Agent, float)]:
    cum_profits = get_cumulative_profits(agent_profits)
    cum_profit_items_sorted = sorted(cum_profits.items(), key=lambda pair: pair[1], reverse=True)
    return cum_profit_items_sorted

def get_cumulative_profits(agent_profits: dict[Agent:List[float]]) -> dict[Agent, float]:
    profits = {}
    for agent, agent_profit in agent_profits.items():  # for loop cycles through the agents and corresponding keys
        cum_profits = np.cumsum(agent_profit)
        profits.update({agent : cum_profits[-1]})
    return profits

@pytest.mark.parametrize('num_agents', [124])
def test_graph_profits(num_agents):
    agents = create_agents(num_agents)
    agent_names = create_agent_names_dict(agents)
    agent_profits = create_agent_profits_dict(agents)
    cumulative_profit_ranking(agent_profits, agent_names)