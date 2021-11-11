import importlib

import click

from agent import Agent
from agents.random_agent import RandomAgent
from demand_function import DemandFunction
from environment import Environment


def main(classname: str, filename: str, timesteps: str):
    agent_import = importlib.import_module(filename)
    agent_impl = getattr(agent_import, classname)
    agent: Agent = agent_impl()

    env = Environment(int(timesteps), DemandFunction())
    env.add_agent(agent)

    for _ in range(10):
        env.add_agent(RandomAgent())
    env.run()
    env.print_results()
    if __name__ == "__main__":
        main()
