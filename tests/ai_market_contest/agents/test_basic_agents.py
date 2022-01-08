from ai_market_contest.agents.fixed_agent_fifty import FixedAgentFifty
from ai_market_contest.agents.fixed_agent_random import FixedAgentRandom
from ai_market_contest.agents.random_agent import RandomAgent

rand_agent = RandomAgent()
fixed_agent_fifty = FixedAgentFifty()
fixed_agent_rand = FixedAgentRandom()


def test_fixed_price_agent_fifty_gives_returns_correct_price():
    first_price = fixed_agent_fifty.policy([], 0)
    second_price = fixed_agent_fifty.policy([], 0)

    fixed_agent_fifty.update([], 0)

    third_price = fixed_agent_fifty.policy([], 0)

    assert first_price == 50
    assert first_price == second_price
    assert first_price == third_price


def test_fixed_random_agent_generates_consistent_prices():
    first_price = fixed_agent_fifty.policy([], 0)
    second_price = fixed_agent_fifty.policy([], 0)

    fixed_agent_fifty.update([], 0)

    third_price = fixed_agent_fifty.policy([], 0)

    assert first_price == second_price
    assert first_price == third_price


def test_random_agent_uses_generates_different_prices():
    first_price = rand_agent.policy([], 0)
    second_price = rand_agent.policy([], 0)

    rand_agent.update([], 0)

    third_price = rand_agent.policy([], 0)

    assert first_price != second_price
    assert first_price != third_price
