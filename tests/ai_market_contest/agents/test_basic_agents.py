from ai_market_contest.agents.fixed_agent import FixedAgent
from ai_market_contest.agents.random_agent import RandomAgent

rand_agent = RandomAgent()
fixed_agent = FixedAgent()

agents = [rand_agent, fixed_agent]


def test_fixed_price_agent_gives_returns_fixed_price():
    first_price = fixed_agent.policy([], 0)
    second_price = fixed_agent.policy([], 0)

    fixed_agent.update([0], 10, [0], 10, 4)

    third_price = fixed_agent.policy([], 0)

    assert first_price == second_price
    assert first_price == third_price


def test_random_agent_uses_generates_different_prices():
    first_price = rand_agent.policy([], 0)
    second_price = rand_agent.policy([], 0)

    rand_agent.update([0], 10, [0], 10, 0)

    third_price = rand_agent.policy([], 0)

    assert first_price != second_price
    assert first_price != third_price
