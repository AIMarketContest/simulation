from ai_market_contest.training.sequential_agent_name_maker import SequentialAgentNameMaker


def test_get_names_functionality():
    agent_name_maker = SequentialAgentNameMaker(10)

    names = agent_name_maker.get_names()

    assert names == [
        "player_0",
        "player_1",
        "player_2",
        "player_3",
        "player_4",
        "player_5",
        "player_6",
        "player_7",
        "player_8",
        "player_9"
    ]


def test_get_name_functionality():
    agent_name_maker = SequentialAgentNameMaker(10)

    for i in range(10):
        name = agent_name_maker.get_name(i)
        assert name == "player_" + str(i)


def test_constructor_validation():
    try:
        SequentialAgentNameMaker(0)
    except ValueError:
        assert True
        return
    assert False


def test_get_name_validation():
    agent_name_maker = SequentialAgentNameMaker(5)
    try:
        agent_name_maker.get_name(-1)
    except ValueError:
        assert True
        try:
            agent_name_maker.get_name(6)
        except ValueError:
            assert True
            return

    assert False


