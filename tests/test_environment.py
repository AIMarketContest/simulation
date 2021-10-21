from unittest import TestCase, mock

import demandfunction
from zero_agent import ZeroAgent
from environment import Environment


class EnvironmentTest(TestCase):
    demand_function = demandfunction.DemandFunction()
    simulation_length = 5

    def test_to_add_agent(self):
        env = Environment(self.simulation_length, self.demand_function)
        a = ZeroAgent()
        env.add_agent(a)
        assert len(env.all_agents) == 1

    def test_to_add_agents(self):
        env = Environment(self.simulation_length, self.demand_function)
        a = ZeroAgent()
        b = ZeroAgent()
        c = ZeroAgent()
        d = ZeroAgent()

        env.add_agent(a)
        env.add_agent(b)
        env.add_agent(c)
        env.add_agent(d)
        assert len(env.all_agents) == 4

    def test_to_get_results(self):
        env = Environment(self.simulation_length, self.demand_function)
        a = ZeroAgent()
        test_set_prices = [{a: 1.00}]
        test_sales = [{a: 4}]
        env.hist_set_prices = test_set_prices
        env.hist_sales_made = test_sales

        prices, sales = env.get_results()
        assert prices == test_set_prices and sales == test_sales

    def test_check_if_runs_simulation_for_correct_duration(self):
        env = Environment(self.simulation_length, self.demand_function)
        with self.assertRaises(IndexError):
            for _ in range(6):
                env.run_next_time_step()

    def test_check_if_gets_price_called_on_time_step(self):
        env = Environment(self.simulation_length, self.demand_function)
        test_agent_a = mock.Mock(spec=ZeroAgent)
        test_agent_b = mock.Mock(spec=ZeroAgent)

        env.add_agent(test_agent_a)
        env.add_agent(test_agent_b)
        env.run_next_time_step()
        test_agent_a.get_initial_price.assert_called_once()
        test_agent_b.get_initial_price.assert_called_once()
        env.run_next_time_step()
        test_agent_a.get_price.assert_called_once()
        test_agent_b.get_price.assert_called_once()
