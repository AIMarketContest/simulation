from ai_market_contest.demand_function import DemandFunction
from typing import Dict


class LowestTakesAllDemandFunction(DemandFunction):
    def __init__(self, max_sales_scale_factor: int = 1000):
        self.max_sales_scale_factor = max_sales_scale_factor

    def get_sales(self, current_prices: Dict[str, int]) -> Dict[str, int]:
        sales: Dict[str, int] = {agent: 0 for agent in current_prices.keys()}
        min_agents = []
        min_price = float("inf")

        for agent, price in current_prices.items():
            if price == min_price:
                min_agents.append(agent)
            elif price < min_price:
                min_agents = [agent]
                min_price = price

        agent_sales = int(self.max_sales_scale_factor / len(min_agents))
        for agent in min_agents:
            sales[agent] = agent_sales

        return sales
