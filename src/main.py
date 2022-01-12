from ai_market_contest.agents.q_agent import QAgent
import dill

agent = QAgent()
dill.dump(agent, open("q_agent.pkl", "wb"))
