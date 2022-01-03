from unittest import TestCase

import numpy as np

from ai_market_contest.agents.fixed_agent_random import FixedAgentRandom # type: ignore
from ai_market_contest.demand_function import DemandFunction # type: ignore
from ai_market_contest.demandfunctions.fixed_demand_function import FixedDemandFunction # type: ignore
from ai_market_contest.environment import Market # type: ignore


class MarketTest(TestCase):
    demand_function: DemandFunction = FixedDemandFunction()
    simulation_length = 5

    def test_to_add_agent(self):
        env = Market(self.simulation_length, self.demand_function, 1)
        a = FixedAgentRandom()
        env.add_agent(a)
        assert len(env.possible_agents) == 1

    def test_to_add_agents(self):
        env = Market(self.simulation_length, self.demand_function, 4)
        a = FixedAgentRandom()
        b = FixedAgentRandom()
        c = FixedAgentRandom()
        d = FixedAgentRandom()

        env.add_agent(a)
        env.add_agent(b)
        env.add_agent(c)
        env.add_agent(d)
        assert len(env.possible_agents) == 4

    def test_to_get_results(self):
        env = Market(self.simulation_length, self.demand_function, 1)
        a = FixedAgentRandom()
        env.add_agent(a)
        test_set_prices = np.array([[1.00]])
        test_sales = np.array([[4]])
        env.hist_set_prices = test_set_prices
        env.hist_sales_made = test_sales

        prices, sales = env.get_results()
        assert prices == test_set_prices and sales == test_sales

    def test_check_if_runs_simulation_for_correct_duration(self):
        env = Market(self.simulation_length, self.demand_function, 0)
        with self.assertRaises(IndexError):
            for _ in range(6):
                env.step({})

    def test_runtime_exception_when_too_many_agents_added(self):
        env = Market(self.simulation_length, self.demand_function, 2)
        env.add_agent(FixedAgentRandom())
        env.add_agent(FixedAgentRandom())

        with self.assertRaises(RuntimeError):
            env.add_agent(FixedAgentRandom())
