from ai_market_contest.agent import Agent

agent = Agent()


def test_initial_price_not_implemented():
    try:
        agent.get_initial_price()
    except NotImplementedError:
        assert True
        return
    assert False


def test_policy_not_implemented():
    try:
        agent.policy([10],0)
    except NotImplementedError:
        assert True
        return
    assert False


def test_update_not_implemented():
    try:
        agent.update(100,0)
    except NotImplementedError:
        assert True
        return
    assert False