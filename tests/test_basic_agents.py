import pytest
from src.random_agent import RandomAgent
from src.fixed_agent import FixedAgent

rand_agent = RandomAgent()
fixed_agent = FixedAgent()


def test_random_agent_gives_different_prices():
    prices = set()
    for i in range(5):
        prices.add(rand_agent.get_price([], 0, 0))
    assert (len(prices) == 5)


def test_random_agent_gives_fixed_initial_price():
    bool_set = set()
    initial_price = rand_agent.get_initial_price()
    for i in range(5):
        bool_set.add(rand_agent.get_initial_price() == initial_price)
    assert (len(bool_set) == 1)


def test_fixed_agent_gives_fixed_initial_price():
    bool_set = set()
    initial_price = fixed_agent.get_initial_price()
    for i in range(5):
        bool_set.add(fixed_agent.get_initial_price() == initial_price)
    assert (len(bool_set) == 1)


def test_fixed_agent_gives_fixed_price():
    bool_set = set()
    price = fixed_agent.get_price([], 0, 0)
    for i in range(5):
        bool_set.add(fixed_agent.get_price([], 0, 0) == price)
    assert (len(bool_set) == 1)
