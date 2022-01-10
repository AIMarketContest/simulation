"""
This file contains the function to represent the results gotten from training agents
"""
from statistics import mean
from typing import Dict, List

import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
import pytest
from matplotlib.ticker import MaxNLocator  # type: ignore
from numpy import ndarray, random
from ray.rllib.policy.policy import Policy

from ai_market_contest.agent import Agent
from ai_market_contest.agents.fixed_agent_random import FixedAgentRandom

matplotlib.use("TkAgg")


def plot_average_step(
    agent_profits: dict[Policy, list[float]],
    agent_names: dict[Policy, str],
    step: int = 1,
) -> plt:
    """
    Function plots all time steps (or averages of timesteps)
    against the profits the agents made
    :agent_prices: dictionary mapping agent to list of profits
    :agent_names: dictionary mapping agent to name of agent
    :step: number of timesteps you want to average
    """
    if step == 0:
        return
    for (
        agent,
        profits,
    ) in (
        agent_profits.items()
    ):  # for loop cycles through the agents and corresponding keys
        start = (1 + step) // 2
        x_axis = list(range(start, len(profits) + 1, step))
        y_axis = range(0, len(profits), step)
        if len(x_axis) < len(y_axis):
            x_axis.append(len(profits))
        if step != 1:
            profits = [
                mean(profits[i : i + step]) for i in range(0, len(profits), step)
            ]
        plt.plot(
            [x + step - start for x in x_axis], profits, label=agent_names.get(agent)
        )
    plt.legend(loc="upper left")
    plt.xlabel("Timestep")
    plt.ylabel("Profit")
    if step == 1:
        plt.title("Time step vs profit")
    else:
        plt.title(f"Rolling average of prior {step} time steps vs profit")
    plt.show()
    return plt


def graph_profits(
    agent_profits: dict[Agent, list[float]], agent_names: dict[Agent, str]
) -> plt:
    """
    This function is used to plot the prices of all agents in the
    input on the same graph against timestep.
    We assume that all the agents run for the same amount of timesteps
    :agent_prices: dictionary mapping agent to list of profits
    :agent_names: dictionary mapping agent to name of agent

    """
    for (
        agent,
        profits,
    ) in (
        agent_profits.items()
    ):  # for loop cycles through the agents and corresponding keys
        x_axis = range(1, len(profits) + 1)
        plt.plot(x_axis, profits, label=agent_names.get(agent))
    plt.legend(loc="upper left")
    plt.xlabel("Time step")
    plt.ylabel("Profit")

    plt.show()
    return plt


def graph_cumulative_profits(
    agent_profits: dict[Agent, list[float]], agent_names: dict[Agent, str]
) -> plt:
    """
    This function is used to plot the total profit that
    each agent makes during a simulation.
    :agent_prices: dictionary mapping agent to list of profits
    :agent_names: dictionary mapping agent to name of agent
    """
    for (
        agent,
        profits,
    ) in (
        agent_profits.items()
    ):  # for loop cycles through the agents and corresponding keys
        x_axis = range(1, len(profits) + 1)
        cum_profits = np.cumsum(profits)
        plt.plot(x_axis, cum_profits, label=agent_names.get(agent))
    plt.legend(loc="upper left")
    plt.xlabel("Time step")
    plt.ylabel("Cumulative Profit")
    plt.title("Cumulative profit over time")

    plt.show()
    return plt


def graph_convergence(
    agent_profits: dict[Agent, list[float]], agent_names: dict[Agent, str]
):
    """
    This function is used to plot the timesteps the different agents convereged at.
    :agent_prices: dictionary mapping agent to list of profits
    :agent_names: dictionary mapping agent to name of agent
    """
    ax = plt.figure().gca()
    x_points = []
    y_points = []
    for agent, profits in agent_profits.items():
        converged_profit = 0
        converged_timestep = 1
        for i in range(len(profits)):
            if converged_profit != profits[i]:
                converged_timestep = i + 1
        x_points.append(agent_names.get(agent))
        y_points.append(converged_timestep)
    ax.bar(x_points, y_points)
    for i, v in enumerate(y_points):
        ax.text(x_points[i], v, str(v))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel("Time step")
    plt.ylabel("Agent")
    plt.title("Time step at which agents converge")
    print(y_points)
    plt.show()


# --------------------- Functions useful for testing  --------------------- #
def create_agents(num_agents: int) -> list[Agent]:
    """
    Function creates a list of agents of specified length
    :num_agents: number of agents in the output list
    :agents: list of agents
    """
    return [FixedAgentRandom() for _ in range(num_agents)]


def create_agent_names_dict(agents: list[Agent]) -> dict[Agent, str]:
    """
    function creates agent_names dict for give number of agents
    :agents: list of agents to map in dictionary
    :output: agent_names is dictionary mapping agent to agent name
    """
    return {agent: f"agent_{i}" for i, agent in enumerate(agents)}


def create_agent_profits_dict(agents: list[Agent]) -> dict[Agent, ndarray]:
    rng = random.default_rng(12345)
    return {agent: rng.integers(low=1, high=100, size=10) for agent in agents}


def create_agent_fixed_profits_dict(
    agents: list[Agent], max_timesteps
) -> dict[Agent, list[float]]:
    agent_profits = {}
    rng = random.default_rng(12345)
    for agent in agents:
        timestep = rng.integers(low=1, high=max_timesteps, size=1)
        profits = rng.integers(low=1, high=101, size=timestep)
        fixed_profits = rng.integers(low=1, high=101, size=1).tolist() * (int)(
            max_timesteps - timestep
        )
        agent_profits[agent] = profits.tolist() + fixed_profits
    return agent_profits


@pytest.mark.parametrize("num_agents", [3, 10, 204, 18])
def test_graph_profits(num_agents):
    agents = create_agents(num_agents)
    agent_names = create_agent_names_dict(agents)
    agent_profits = create_agent_profits_dict(agents)
    plot = graph_profits(agent_profits, agent_names)
    plot.show()


@pytest.mark.parametrize("num_agents,step", [(3, 5), (10, 3), (24, 1)])
def test_graph_average_profits(num_agents, step):
    agents = create_agents(num_agents)
    agent_names = create_agent_names_dict(agents)
    agent_profits = create_agent_profits_dict(agents)
    plot = plot_average_step(agent_profits, agent_names, step)
    plot.show()


def test_graph_convergence(num_agents=5):
    agents = create_agents(num_agents)
    agent_names = create_agent_names_dict(agents)
    agent_profits = create_agent_fixed_profits_dict(agents, 20)
    graph_convergence(agent_profits, agent_names)


def test_graph_cumulative_profit(num_agents=5):
    agents = create_agents(num_agents)
    agent_names = create_agent_names_dict(agents)
    agent_profits = create_agent_fixed_profits_dict(agents, 20)
    graph_cumulative_profits(agent_profits, agent_names)
