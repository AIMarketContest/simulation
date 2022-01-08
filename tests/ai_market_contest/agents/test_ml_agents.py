from ai_market_contest.agents.q_agent import QAgent
from ai_market_contest.agents.sarsa_agent import SarsaAgent

# TODO :: Make these tests pass (I believe the issue is that the state for Q table includes its own price, meaning it
#  essentially just prices itself into whatever was most recently used as the price). Moreover it's using a formula to
#  update the Q Table with the reward value (in update) in a way that favours repeated attempts on the same number, even
#  if the corresponding reward is low


def test_q_learning_agent_sets_highest_price_under_fixed_demand():
    q_agent = QAgent()

    price = 0
    for i in range(100):
        price = q_agent.policy([price, 50], 0)
        q_agent.update(price * 100, 0)
    assert price >= 95


def test_sarsa_agent_sets_highest_price_under_fixed_demand():
    sarsa_agent = SarsaAgent()

    price = 0
    for i in range(100):
        price = sarsa_agent.policy([price, 50], 0)
        sarsa_agent.update(price * 100, 0)
    assert price >= 95
