from typing import Any, Callable, Dict  # type: ignore


class PolicySelector:
    """
    Determines the function that maps
    the agent id to a policy for training.

    Attributes
    ----------
    agent_name: str
        A string representing the name of the agent to be trained.
    self_play_number: int
        Number of self-play agents to be trained against.
    naive_agents_counts: Dict[str, int]
        Map from an agent name to the number of that agent to be trained against.


    """

    def __init__(
        self,
        agent_name: str = "rl-agent",
        self_play_number: int = 0,
        naive_agents_counts: Dict[str, int] = {},
    ):
        self.agent_name = agent_name
        self.self_play_number = self_play_number
        self.naive_agents_counts = naive_agents_counts
        self.opponent_name = self.get_agent_opponent_name()

    def get_agent_opponent_name(self):
        return self.agent_name + "-opponent"

    def get_agent_name(self):
        return self.agent_name

    def has_self_play(self):
        return self.self_play_number > 0

    def get_naive_agents_names(self):
        return self.naive_agents_counts.keys()

    def get_select_policy_function(self) -> Callable[[str, Any, Any], str]:  # type: ignore
        """
        Returns a function that maps an agent_id to a policy name.

        Returns
        -------
        Callable[[int, Any, Any], str]
            Function that maps an agent_id to a policy name.
        """

        def select_policy(agent_id: str, *args, **kwargs) -> str:
            if agent_id == "player_0":
                return self.agent_name

            if agent_id in [
                "player_" + str(i) for i in range(1, self.self_play_number + 1)
            ]:
                return self.opponent_name
            cur_number_of_agents = self.self_play_number + 1
            for naive_agent, count in self.naive_agents_counts.items():
                if agent_id in [
                    "player_" + str(i)
                    for i in range(
                        cur_number_of_agents, cur_number_of_agents + count + 1
                    )
                ]:
                    return naive_agent
                cur_number_of_agents += count

        return select_policy
