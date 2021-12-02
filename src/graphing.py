"""
This file contains the function to represent the results gotten from training agents
"""
from typing import List
import pytest
from ai_market_contest.agents import fixed_agent
from ai_market_contest.agent import Agent
import matplotlib.pyplot as plt
from numpy import random
from statistics import mean


def plot_average_step(agent_profits: dict[Agent:List[float]], agent_names: dict[Agent:str], step: int = 1) -> plt:
    """
    Function plots all time steps (or averages of timesteps) against the profits the agents made
    :agent_prices: dictionary mapping agent to list of profits
    :agent_names: dictionary mapping agent to name of agent
    :step: number of timesteps you want to average
    """
    if step == 0:
        return
    for agent, profits in agent_profits.items():  # for loop cycles through the agents and corresponding keys
        start = -1 * (-(1+step) // 2)
        x_axis = list(range(start, len(profits) + 1, step))
        y_axis = range(0, len(profits), step)
        if len(x_axis) < len(y_axis):
            x_axis.append(len(profits))
        print(list(x_axis))
        if step != 1:
            profits = [mean(profits[i:i + step]) for i in range(0, len(profits), step)]
        plt.plot(x_axis, profits, label=agent_names.get(agent))
    plt.legend(loc="upper left")
    plt.xlabel("Timestep")
    plt.ylabel("Profit")
    if step == 1:
        plt.title("Time step vs profit")
    else:
        plt.title(f'Average of {step} time steps vs profit')
    plt.show()
    return plt



def graph_profits(agent_profits: dict[Agent:List[float]], agent_names: dict[Agent:str]) -> plt:
    """
    This function is used to plot the prices of all agents in the input on the same graph against timestep.
    We assume that all the agents run for the same amount of timesteps
    :agent_prices: dictionary mapping agent to list of profits
    :agent_names: dictionary mapping agent to name of agent

    """

    for agent, profits in agent_profits.items():  # for loop cycles through the agents and corresponding keys
        x_axis = range(1, len(profits) + 1)
        plt.plot(x_axis, profits, label=agent_names.get(agent))
    plt.legend(loc="upper left")
    plt.xlabel("Time step")
    plt.ylabel("Profit")

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
    rng = random.default_rng(12345)
    for i in range(num_agents):
        agent_profits.update({agents[i]: rng.integers(low=1, high=101, size=10)})
    return agent_profits


@pytest.mark.parametrize('num_agents', [3,10, 204, 18])
def test_graph_profits(num_agents):
    agents = create_agents(num_agents)
    agent_names = create_agent_names_dict(agents)
    agent_profits = create_agent_profits_dict(agents)
    plot = graph_profits(agent_profits, agent_names)
    plot.show()


@pytest.mark.parametrize('num_agents,step',[(3,5)])
def test_graph_average_profits(num_agents,step):
    agents = create_agents(num_agents)
    agent_names = create_agent_names_dict(agents)
    agent_profits = create_agent_profits_dict(agents)
    plot = plot_average_step(agent_profits, agent_names,step)
    plot.show()