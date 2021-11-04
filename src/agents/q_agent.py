from agent import Agent
from environment import Environment

class QAgent(Agent):
    def __init__(self, env: Environment):
        self.curr_price = 0
        self.env = env
        self.cost = 0.3
        self.env.add_agent(self)

    def policy(self, state: list[float]) -> float:
        return self.curr_price

    def get_reward(self, demand: float) -> float:
        return (self.curr_price - self.cost) * demand
    
    def update(
        self,
        last_round_agents_prices: list[float],
        last_round_sales: int,
        identity_index: int,
    ) -> None:
        return