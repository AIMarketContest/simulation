from unittest import TestCase, mock

from agent import Agent
import demandfunction
import environment as env


class EnvironmentTest(TestCase):
    demand_function = demandfunction.DemandFunction()
    simulation_length = 5

    def test_to_add_agent(self):
        ev = env.Environment(self.simulation_length, self.demand_function)
        a = Agent()
        ev.add_agent(a)
        assert len(ev.all_agents) == 1

    def test_to_add_agents(self):
        ev = env.Environment(self.simulation_length, self.demand_function)
        a = Agent()
        ev.add_agent(a)
        ev.add_agent(a)
        ev.add_agent(a)
        ev.add_agent(a)
        assert len(ev.all_agents) == 4

    def test_to_get_results(self):
        ev = env.Environment(self.simulation_length, self.demand_function)
        a = Agent()
        dict_price = {a: 1.00}
        dict_sales = {a: 4}
        ev.hist_set_prices = dict_price
        ev.hist_sales_made = dict_sales

        prices, sales = ev.get_results()
        assert prices == dict_price and sales == dict_sales

    def test_check_if_runs_simulation_for_correct_duration(self):
        ev = env.Environment(self.simulation_length, self.demand_function)
        with self.assertRaises(IndexError):
            for _ in range(6):
                ev.run_next_time_step()

    def test_check_if_rnts_gets_price_all_agents(self):
        ev = env.Environment(self.simulation_length, self.demand_function)
        test_agent_a = mock.Mock()
        test_agent_b = mock.Mock()

        ev.add_agent(test_agent_a)
        ev.add_agent(test_agent_b)
        ev.run_next_time_step()
        test_agent_a.get_price.assert_called_once()
        test_agent_b.get_price.assert_called_once()
