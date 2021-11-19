import importlib

from ai_market_contest.agent import Agent
from ai_market_contest.agents.random_agent import RandomAgent
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction
from ai_market_contest.environment import init_env


def main(classname: str, filename: str, timesteps: str):
    agent_import = importlib.import_module(filename)
    agent_impl = getattr(agent_import, classname)
    agent: Agent = agent_impl()

    env = init_env(int(timesteps), FixedDemandFunction(), 10)
    env.add_agent(agent)

    for _ in range(10):
        env.add_agent(RandomAgent())
