from typing import Optional

import questionary


def choose_an_agent_from(agent_names: list[str], action: str) -> Optional[str]:
    agent_name = questionary.select(
        f"Choose an agent to {action}.", choices=agent_names
    ).ask()
    return agent_name


def choose_an_agent_version_from(
    agent_versions: list[str], action: str
) -> Optional[str]:
    chosen_trained_agent: str = questionary.select(
        f"Select which version of the agent would you like to {action}",
        choices=agent_versions,
    ).ask()
    return chosen_trained_agent


def choose_a_training_configuration(training_configs: str) -> Optional[str]:
    training_config: str = questionary.select(
        "Choose a training config:", choices=training_configs
    ).ask()
    return training_config
