from unittest import TestCase, mock

import numpy as np

from agents.fixed_agent import FixedAgent
from demandfunctions.fixed_demand_function import FixedDemandFunction
from environment import Environment


class EnvironmentTest(TestCase):
    demand_function = FixedDemandFunction()
    simulation_length = 5

    def test_to_add_agent(self):
        env = Environment(self.simulation_length, self.demand_function, 1)
        a = FixedAgent()
        env.add_agent(a)
        assert len(env.all_agents) == 1

    def test_to_add_agents(self):
        env = Environment(self.simulation_length, self.demand_function, 4)
        a = FixedAgent()
        b = FixedAgent()
        c = FixedAgent()
        d = FixedAgent()

        env.add_agent(a)
        env.add_agent(b)
        env.add_agent(c)
        env.add_agent(d)
        assert len(env.all_agents) == 4

    def test_to_get_results(self):
        env = Environment(self.simulation_length, self.demand_function, 1)
        a = FixedAgent()
        env.add_agent(a)
        test_set_prices = np.array([[1.00]])
        test_sales = np.array([[4]])
        env.hist_set_prices = test_set_prices
        env.hist_sales_made = test_sales

        prices, sales = env.get_results()
        assert prices == test_set_prices and sales == test_sales

    def test_check_if_runs_simulation_for_correct_duration(self):
        env = Environment(self.simulation_length, self.demand_function, 0)
        with self.assertRaises(IndexError):
            for _ in range(6):
                env.run_next_time_step()

    def test_check_if_gets_price_called_on_time_step(self):
        env = Environment(self.simulation_length, self.demand_function, 2)
        test_agent_a = mock.Mock(spec=FixedAgent)
        test_agent_b = mock.Mock(spec=FixedAgent)
        test_agent_a.configure_mock(
            **{"get_initial_price.return_value": 2.0, "get_price.return_value": 3.3}
        )
        test_agent_b.configure_mock(
            **{"get_initial_price.return_value": 2.5, "get_price.return_value": 1.3}
        )

        env.add_agent(test_agent_a)
        env.add_agent(test_agent_b)
        env.run_next_time_step()
        test_agent_a.get_initial_price.assert_called_once()
        test_agent_b.get_initial_price.assert_called_once()
        env.run_next_time_step()
        test_agent_a.get_price.assert_called_once()
        test_agent_b.get_price.assert_called_once()
