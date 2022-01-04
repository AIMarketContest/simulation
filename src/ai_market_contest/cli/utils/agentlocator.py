from ast import literal_eval
import pathlib
import importlib.util
from configparser import ConfigParser
from typing import List
from ai_market_contest.cli.cli_config import CONFIG_FILENAME, CUR_AGENTS
from ai_market_contest.agent import Agent


class AgentLocator:
    def __init__(self, agents_dir: pathlib.Path):
        self.agents_dir = agents_dir

    def _get_agents(self) -> List[str]:
        config_parser: ConfigParser = ConfigParser()
        config_parser.read(self.agents_dir / CONFIG_FILENAME)
        agents: List[str] = literal_eval(
            config_parser["agentsironment"]["demand functions"]
        )
        return agents

    def get_agent(self, agent_name: str) -> DemandFunction:
        if agent_name in CUR_AGENTS:
            return CUR_AGENTS[agent_name]
        agent_dir: pathlib.Path = self.agents_dir / agent_name
        agent_file: str = agent_dir / agent_name + ".py"
        spec = importlib.util.spec_from_file_location(agent_name, agent_file)
        if spec.loader is None:
            raise Exception("Error in finding the required agent")
        spec.loader.exec_module(demand_func_module)  # type: ignore
        agent_cls = getattr(demand_func_module, agent_name)  # type: ignore
        return agent_cls