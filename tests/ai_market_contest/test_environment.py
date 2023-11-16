import math
from unittest import TestCase

from ai_market_contest.demand_function import DemandFunction  # type: ignore
from ai_market_contest.demandfunctions.fixed_demand_function import (
    FixedDemandFunction,  # type: ignore
)
from ai_market_contest.environment import Market  # type: ignore
from ai_market_contest.training.sequential_agent_name_maker import (
    SequentialAgentNameMaker,
)


class MarketTest(TestCase):
    simulation_length = 5
    num_agents = 2

    demand_function: DemandFunction = FixedDemandFunction()
    agent_name_maker = SequentialAgentNameMaker(num_agents)

    def test_environment_setup(self):
        env = Market(
            self.demand_function,
            self.simulation_length,
            self.agent_name_maker,
        )
        assert env.reward_range == (-math.inf, math.inf)
        assert env.done is False
        assert env.time_step == 0

    def test_environment_reset(self):
        env = Market(
            self.demand_function,
            self.simulation_length,
            self.agent_name_maker,
        )

        env.step({"player_0": 1, "player_1": 3})
        assert env.time_step != 0

        env.reset()
        assert env.time_step == 0

    def test_environment_handles_step_correctly(self):
        env = Market(
            self.demand_function,
            self.simulation_length,
            self.agent_name_maker,
        )

        observations, rewards, dones, infos = env.step({"player_0": 1, "player_1": 3})
        assert observations == {"player_0": [1, 3], "player_1": [1, 3]}
        assert rewards == {"player_0": 1, "player_1": 3}
        assert dones == {"__all__": False}
        assert infos == {
            "player_0": {"identity_index": 0},
            "player_1": {"identity_index": 1},
        }
        observations, rewards, dones, infos = env.step({"player_0": 2, "player_1": 3})
        assert observations == {"player_0": [2, 3], "player_1": [2, 3]}
        assert rewards == {"player_0": 2, "player_1": 3}
        assert dones == {"__all__": False}
        assert infos == {
            "player_0": {"identity_index": 0},
            "player_1": {"identity_index": 1},
        }
        observations, rewards, dones, infos = env.step({"player_0": 2, "player_1": 2})
        assert observations == {"player_0": [2, 2], "player_1": [2, 2]}
        assert rewards == {"player_0": 2, "player_1": 2}
        assert dones == {"__all__": False}
        assert infos == {
            "player_0": {"identity_index": 0},
            "player_1": {"identity_index": 1},
        }
        observations, rewards, dones, infos = env.step({"player_0": 1, "player_1": 2})
        assert observations == {"player_0": [1, 2], "player_1": [1, 2]}
        assert rewards == {"player_0": 1, "player_1": 2}
        assert dones == {"__all__": False}
        assert infos == {
            "player_0": {"identity_index": 0},
            "player_1": {"identity_index": 1},
        }
        observations, rewards, dones, infos = env.step({"player_0": 3, "player_1": 1})
        assert observations == {"player_0": [3, 1], "player_1": [3, 1]}
        assert rewards == {"player_0": 3, "player_1": 1}
        assert dones == {"__all__": True}
        assert infos == {
            "player_0": {"identity_index": 0},
            "player_1": {"identity_index": 1},
        }

        assert env.done is True
