import pathlib

from ai_market_contest.cli.cli_config import HASH_LENGTH  # type: ignore
from ai_market_contest.cli.utils.processmetafile import get_trained_agent_metadata


def display_trained_agents(agent_dir: pathlib.Path, trained_agents: list[str]):
    for index, trained_agent in enumerate(trained_agents):
        (agent_hash, time, msg, parent_hash) = get_trained_agent_metadata(
            agent_dir, trained_agent
        )
        shortened_hash: str = agent_hash[:HASH_LENGTH]
        print(f"\n{index} {shortened_hash} {str(time)} {msg}")


def display_agents(agents: list[str]):
    print("The current agents are: ")
    print(f"[{', '.join(agents)}]")

def display_training_configs(training_configs: list[str]):
    print("The current training configs are:")
    print(f"[{', '.join(training_configs)}]")