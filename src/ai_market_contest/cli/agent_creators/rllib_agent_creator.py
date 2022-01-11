import pathlib
from ast import literal_eval
from configparser import ConfigParser
from typing import List

from ai_market_contest.cli.agent_creators.agent_creator import AgentCreator
from ai_market_contest.cli.utils.hashing import set_agent_initial_hash
from ai_market_contest.cli.utils.initialiseagent import make_initial_trained_agent


class RLlibAgentCreator(AgentCreator):
    def __init__(self, path: pathlib.Path, agent_names: List[str]):
        super().__init__(path, agent_names)
        self.agent = agent_names[0]
        self.agent_dir = self.agents_dir / self.agent

    def make_agent_folder(self):
        self.agent_dir.mkdir(parents=True, exist_ok=True)
        initial_hash: str = set_agent_initial_hash(self.agent_dir)
        make_initial_trained_agent(self.agent_dir, self.agent, initial_hash)

    def update_agents_config_file(self):
        config_parser: ConfigParser = ConfigParser()
        config_parser.optionxform = str
        config_parser.read(self.agents_config_file)
        custom_agents: List[str] = literal_eval(config_parser["agents"]["rllibagents"])
        custom_agents += self.agents
        config_parser["agents"]["rllibagents"] = str(custom_agents)
        with self.agents_config_file.open("w") as agents_config_file:
            config_parser.write(agents_config_file)

    def create_agents(self):
        self.make_agent_folder()
        self.update_agents_config_file()
