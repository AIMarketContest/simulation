from agents.fixed_agent import FixedAgent
from agents.random_agent import RandomAgent

rand_agent = RandomAgent()
fixed_agent = FixedAgent()

agents = [rand_agent, fixed_agent]


def test_fixed_price_agent_gives_returns_fixed_price():
    first_inital_price = fixed_agent.get_initial_price()
    second_initial_price = fixed_agent.get_initial_price()

    assert first_inital_price == second_initial_price

    first_price = fixed_agent.get_price([0], 10, 0)
    second_price = fixed_agent.get_price([0], 10, 0)

    assert first_price == second_price


def test_random_agent_uses_generates_different_prices():
    first_inital_price = rand_agent.get_initial_price()
    second_initial_price = rand_agent.get_initial_price()

    assert first_inital_price != second_initial_price

    first_price = rand_agent.get_price([0], 10, 0)
    second_price = rand_agent.get_price([0], 10, 0)

    assert first_price != second_price
