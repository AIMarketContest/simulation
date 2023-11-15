from typing import Optional

import questionary


def choose_an_agent_to(action: str, agent_names: list[str]) -> Optional[str]:
    agent_name = questionary.select(
        f"Choose an agent to {action}.", choices=agent_names
    ).ask()
    if not agent_name:
        return
    return agent_name
