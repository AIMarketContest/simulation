from src.agent import Agent
from src.demandfunction import Demand_Function

class Environment:
    def __self__(self, time_steps: int, demand: Demand_Function):
        self.lst_agents = []
        self.lst_sales = []
        self.lst_prices = []
        self.time_steps = time_steps
        self.demand = demand

    def add_agent(self, agent: Agent) -> None:
        self.lst_agents.append(agent)

    # returns (list of prices set, list of units sold)
    def get_results(self) -> (list[dict[Agent, float]], list[dict[Agent, int]]):
        return self.lst_prices, self.lst_sales

    def run_next_time_step(self) -> None:
        current_prices = {}
        prior_sales = self.lst_sales[-1]

        for agent in self.lst_agents:
            prior_sales_for_agent = prior_sales [agent]
            current_prices[agent] = agent.get_price(self.lst_prices, prior_sales_for_agent)

        self.lst_prices.append(current_prices)
        self.lst_sales.append(self.demand.get_sales(current_prices))