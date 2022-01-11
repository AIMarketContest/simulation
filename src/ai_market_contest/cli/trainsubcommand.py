import sys

from ai_market_contest.cli.utils.hashing import get_shortened_hashes


def ask_for_trained_agents(agent: str) -> bool:
    max_count = 3
    count = 0
    while count < max_count:
        char = input("Would you like to train a trained version of the agent (y/n): ")
        if char == "n" or char == "y":
            return True if char == "y" else False
    print("Operation aborted: failed to get valid input")
    sys.exit(1)


def choose_training_config(training_configs: list[str]):
    print("Choose a training config: ", end="")
    while True:
        chosen_config = input()
        if chosen_config in training_configs:
            break
        print(f"{chosen_config} not an existing training config")
        print("Choose a valid agent to train: ")
    return chosen_config


def choose_trained_agent(trained_agents: list[str]):
    shortened_hashes = get_shortened_hashes(trained_agents)
    max_count = 3
    count = 0
    print(
        "\nInput the hash or index of the version of the agent to be trained: ", end=""
    )
    while count < max_count:
        count += 1
        trained_agent = input()
        if trained_agent in trained_agents or trained_agent in shortened_hashes:
            break
        if trained_agent.isnumeric():
            if int(trained_agent) in range(len(trained_agents)):
                index = int(trained_agent)
                trained_agent = trained_agents[index]
                break
        print(
            f"Hash or index {trained_agent} does not correspond to an existing ",
            "version of the agent",
        )
        print(
            "Enter a valid hash or index of the version of the agent to be trained: ",
            end="",
        )
    if count >= max_count:
        print("\nOperation Aborted: Invalid hash or index")
        sys.exit(1)
    return trained_agent
