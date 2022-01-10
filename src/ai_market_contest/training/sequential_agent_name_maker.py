from ai_market_contest.training.agent_name_maker import AgentNameMaker  # type: ignore


class SequentialAgentNameMaker(AgentNameMaker):
    MIN_NUM_AGENTS = 1

    def __init__(self, number_of_agents):
        if number_of_agents < self.MIN_NUM_AGENTS:
            raise ValueError(f"Cannot have less than {self.MIN_NUM_AGENTS} agents")

        self.number_of_agents = number_of_agents

    def get_names(self) -> list[str]:
        return [f"player_{i}" for i in range(self.number_of_agents)]

    def get_name(self, num: int) -> str:
        if num < 0 or num >= self.number_of_agents:
            raise ValueError(
                f"Agent index {num} is out of range, should be between 0 and {self.number_of_agents - 1}"
            )
        return f"player_{num}"
