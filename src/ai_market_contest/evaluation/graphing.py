"""
This file contains the function to represent the results gotten from training agents
"""
from statistics import mean

import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
from matplotlib.ticker import MaxNLocator  # type: ignore
from ray.rllib.policy.policy import Policy

from ai_market_contest.agent import Agent

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
):
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


def graph_cumulative_profits(
    agent_profits: dict[str, list[int]], agent_names: dict[str, str]
):
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
        plt.plot(x_axis, cum_profits, label=agent_names[agent])
    plt.legend(loc="upper left")
    plt.xlabel("Time step")
    plt.ylabel("Cumulative Profit")
    plt.title("Cumulative profit over time")

    plt.show()


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
