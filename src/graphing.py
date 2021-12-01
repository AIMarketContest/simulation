"""
This file contains the function to represent the results gotten from training agents
"""
from typing import List
import pytest
from ai_market_contest.agents import fixed_agent
from ai_market_contest.agent import Agent
import matplotlib.pyplot as plt
from numpy import random


def graph_profits(agent_profits: dict[Agent:List[float]], agent_names: dict[Agent:str]) -> plt:
    """
    This function is used to plot the prices of all agents in the input on the same graph against timestep
    :agent_prices: dictionary mapping agent to list of profits
    :agent_names: dictionary mapping agent to name of agent
    """
    for agent, profits in agent_profits.items():  # for loop cycles through the agents and corresponding keys
        plt.plot(len(agent_profits), profits, label=agent_names.get(agent))
    plt.show()
    return plt


def create_agents(num_agents: int) -> List[Agent]:
    """
    Function creates a list of agents of specified length
    :num_agents: number of agents in the output list
    :agents: list of agents
    """
    agents = []
    for i in range(num_agents):
        agents.append(fixed_agent.FixedAgent())
    return agents


def create_agent_names_dict(agents: List[Agent]) -> dict[Agent:List[str]]:
    """
    function creates agent_names dict for give number of agents
    :agents: list of agents to map in dictionary
    :output: agent_names is dictionary mapping agent to agent name
    """
    agent_names = {}
    num_agents = len(agents)
    for i in range(num_agents):
        agent_names.update({agents[i]: f'agent_{i}'})
    return agent_names


def create_agent_profits_dict(agents: List[Agent]) -> dict[Agent:List[float]]:
    agent_profits = {}
    num_agents = len(agents)
    for i in range(num_agents):
        agent_profits.update({agents[i]: random.randint(0, 101)})
    return agent_profits


@pytest.mark.parametrize('num_agents', [20, 204, 18])
def test_graph_profits(num_agents):
    agents = create_agents(num_agents)
    agent_names = create_agent_names_dict(agents)
    agent_profits = create_agent_profits_dict(agents)
    plot = graph_profits(agent_profits, agent_names)
    plot.show()
