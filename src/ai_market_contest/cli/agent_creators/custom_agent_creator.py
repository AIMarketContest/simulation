import pathlib
from ast import literal_eval
from configparser import ConfigParser
from typing import List

from ai_market_contest.cli.agent_creators.agent_creator import (
    AgentCreator,  # type: ignore
)
from ai_market_contest.cli.utils.hashing import set_agent_initial_hash
from ai_market_contest.cli.utils.initialiseagent import (
    create_new_agent_file,
    make_initial_trained_agent,
)


class CustomAgentCreator(AgentCreator):
    def make_agents_classes(self):
        for agent in self.agents:
            self.create_agent_class(agent)

    def create_agent_class(self, agent_name: str):
        agent_dir: pathlib.Path = self.agents_dir / agent_name
        agent_filename: str = f"{agent_name}.py"
        agent_file: pathlib.Path = agent_dir / agent_filename
        agent_dir.mkdir(parents=True, exist_ok=True)
        agent_file.touch()
        create_new_agent_file(agent_file, agent_name)
        initial_hash: str = set_agent_initial_hash(agent_dir)
        make_initial_trained_agent(agent_dir, agent_name, initial_hash)

    def update_agents_config_file(self):
        config_parser: ConfigParser = ConfigParser()
        config_parser.optionxform = str
        config_parser.read(self.agents_config_file)
        custom_agents: List[str] = literal_eval(config_parser["agents"]["customagents"])
        custom_agents += self.agents
        config_parser["agents"]["customagents"] = str(custom_agents)
        with self.agents_config_file.open("w") as agents_config_file:
            config_parser.write(agents_config_file)

    def create_agents(self):
        self.make_agents_classes()
        self.update_agents_config_file()
