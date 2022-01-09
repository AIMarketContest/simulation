from ai_market_contest.training.policy_selector import PolicySelector

def test_constructor_and_getter_methods():
    policy_selector = PolicySelector(
        "a super smart machine learning agent that makes stacks of cash",
        10,
        {"a very dumb naive agent": 4}
    )

    assert policy_selector.get_agent_opponent_name() == \
           "a super smart machine learning agent that makes stacks of cash-opponent"
    assert policy_selector.get_agent_name() == \
           "a super smart machine learning agent that makes stacks of cash"
    assert policy_selector.has_self_play() is True

    naive_agents_names = policy_selector.get_naive_agents_names()

    assert "a very dumb naive agent" in naive_agents_names
    assert len(naive_agents_names) == 1

def test_policy_select_function():
    policy_selector = PolicySelector(
        "a super smart machine learning agent that makes stacks of cash",
        10,
        {"a very dumb naive agent": 4}
    )

    select_policy = policy_selector.get_select_policy_function()

    # TODO :: test `select_policy`
