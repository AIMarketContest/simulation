from ai_market_contest.cli.utils.inputagentname import (
    remove_underscores,
    is_valid_agent_name,
)


def test_remove_underscores():
    assert remove_underscores("hello_123") == "hello123"
    assert remove_underscores("1_2_3_4_5") == "12345"
    assert remove_underscores("1234") == "1234"


def test_is_valid_agent_name():
    assert is_valid_agent_name("1_player") == False
    assert is_valid_agent_name("agent-1") == False
    assert is_valid_agent_name("agent_1") == True
