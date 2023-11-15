from typing import Optional

import ai_market_contest.cli.user_interactions.questionary_interactions as ask_user_to
from ai_market_contest.cli.utils.existing_agent.existing_agent import ExistingAgent
from ai_market_contest.cli.utils.get_agents import get_agent_names


def select_existing_agent(path: str) -> Optional[ExistingAgent]:
    agent_names: list[str] = get_agent_names(path)
    chosen_agent_name: str = ask_user_to.choose_an_agent_to("train", agent_names)
    if not chosen_agent_name:
        return
    chosen_agent: ExistingAgent = ExistingAgent(chosen_agent_name, path)
    return chosen_agent
