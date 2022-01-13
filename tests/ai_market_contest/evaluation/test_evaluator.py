from ai_market_contest.evaluation.ranking import (
    cumulative_profit_ranking,
    get_cumulative_profits,
)


def test_cumulative_profit_ranking():
    res = cumulative_profit_ranking(
        {"A1": [1, 2, 3, 4], "A2": [2, 2, 2, 2], "A3": [5, 4, 0, 0]}
    )
    assert res == [("A1", 10), ("A3", 9), ("A2", 8)]


def test_get_cumulative_profits():
    res = get_cumulative_profits(
        {"A1": [1, 2, 3, 4], "A2": [2, 2, 2, 2], "A3": [5, 4, 0, 0]}
    )
    assert res == {"A1": 10, "A3": 9, "A2": 8}


# def test_get_agent_name_mapping():
#     agent1 = FixedAgentFifty
#     agent2 = FixedAgentFifty
#     res = get_agent_name_mapping([agent1, agent2], ["A1", "A2"])
#     assert res == {"A1": "FixedAgentFifty 1", "A2": "FixedAgentFifty 2"}
