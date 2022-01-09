import pathlib

from ai_market_contest.cli.cli_config import HASH_LENGTH  # type: ignore


def display_trained_agents(agent_dir: pathlib.Path, trained_agents: list[str]):
    trained_agents_info = get_trained_agents_info(trained_agents, agent_dir)
    for index, trained_agent_info in enumerate(trained_agents_info):
        print(f"\n{index} {trained_agent_info}")


def display_agents(agents: list[str]):
    print("The current agents are: ")
    print(f"[{', '.join(agents)}]")


def display_training_configs(training_configs: list[str]):
    print("The current training configs are:")
    print(f"[{', '.join(training_configs)}]")
